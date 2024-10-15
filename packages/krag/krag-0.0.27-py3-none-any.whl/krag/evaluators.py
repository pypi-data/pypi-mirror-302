# krag/evaluators.py

from typing import Union, List, Dict, Optional
from enum import Enum
import math
from functools import lru_cache
from krag.document import KragDocument as Document
from korouge_score import rouge_scorer
from kiwipiepy import Kiwi
import numpy as np
import matplotlib.pyplot as plt

class AveragingMethod(Enum):
    MICRO = "micro"
    MACRO = "macro"
    BOTH = "both"

class MatchingCriteria(Enum):
    ALL = "all"
    PARTIAL = "partial"

 
 

class OfflineRetrievalEvaluators:
    def __init__(self, actual_docs: List[List[Document]], predicted_docs: List[List[Document]], 
                 match_method: str = "text", averaging_method: AveragingMethod = AveragingMethod.BOTH, 
                 matching_criteria: MatchingCriteria = MatchingCriteria.ALL) -> None:
        """
        OfflineRetrievalEvaluators 클래스를 초기화합니다.

        Args:
            actual_docs (List[List[Document]]): 실제 문서 리스트의 리스트
            predicted_docs (List[List[Document]]): 예측된 문서 리스트의 리스트
            match_method (str, optional): 문서 매칭 방법. 기본값은 "text"
            averaging_method (AveragingMethod, optional): 결과 평균 계산 방법. 기본값은 AveragingMethod.BOTH
            matching_criteria (MatchingCriteria, optional): 히트로 간주할 기준. 기본값은 MatchingCriteria.ALL

        Raises:
            ValueError: 입력 리스트가 비어있거나 길이가 다를 경우 발생
        """
        if not actual_docs or not predicted_docs:
            raise ValueError("입력 문서 리스트가 비어있을 수 없습니다.")
        if len(actual_docs) != len(predicted_docs):
            raise ValueError("실제 문서 리스트와 예측 문서 리스트의 길이가 같아야 합니다.")
        
        self.actual_docs = actual_docs 
        self.predicted_docs = predicted_docs  
        self.match_method = match_method
        self.averaging_method = averaging_method
        self.matching_criteria = matching_criteria
        self._cache = {}

    @lru_cache(maxsize=1000)
    def text_match(self, actual_text: str, predicted_text: Union[str, List[str]]) -> bool:
        """
        실제 텍스트가 예측 텍스트와 일치하는지 확인합니다.

        Args:
            actual_text (str): 실제 텍스트
            predicted_text (Union[str, List[str]]): 예측 텍스트 또는 텍스트 리스트

        Returns:
            bool: 일치하면 True, 그렇지 않으면 False
        """
        if isinstance(predicted_text, list):
            return any(actual_text in text for text in predicted_text)
        return actual_text in predicted_text


    def calculate_hit_rate(self, k: Optional[int] = None) -> Dict[str, float]:
        """
        검색된 문서의 적중률을 계산합니다.

        Args:
            k (Optional[int], optional): 고려할 상위 문서 수. 기본값은 None

        Returns:
            Dict[str, float]: 적중률 딕셔너리
        """
        hit_count = 0
        for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs):
            predicted_texts = [pred_doc.page_content for pred_doc in predicted_docs[:k]]
            if self.matching_criteria == MatchingCriteria.ALL:
                hit = all(any(self.text_match(actual_doc.page_content, pred_text) for pred_text in predicted_texts) for actual_doc in actual_docs)
            else:  # PARTIAL
                hit = any(any(self.text_match(actual_doc.page_content, pred_text) for pred_text in predicted_texts) for actual_doc in actual_docs)
            hit_count += hit

        hit_rate = hit_count / len(self.actual_docs)
        return {"hit_rate": hit_rate}
    


    def calculate_precision(self, k: Optional[int] = None) -> Dict[str, float]:
        """
        검색된 문서의 정밀도를 계산합니다.

        Args:
            k (Optional[int], optional): 고려할 상위 문서 수. 기본값은 None

        Returns:
            Dict[str, float]: 정밀도 딕셔너리
        """

        micro_precision = 0
        macro_precisions = []

        for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs):
            k_effective = min(k or len(predicted_docs), len(predicted_docs))
            relevant_count = sum(
                1 for predicted_doc in predicted_docs[:k_effective]
                if any(self.text_match(actual_doc.page_content, predicted_doc.page_content) for actual_doc in actual_docs)
            )
            micro_precision += relevant_count
            macro_precisions.append(relevant_count / k_effective if k_effective > 0 else 0)

        total_predicted = sum(min(k or len(predicted_docs), len(predicted_docs)) for predicted_docs in self.predicted_docs)
        
        return {
            "micro_precision": micro_precision / total_predicted if total_predicted > 0 else 0.0,
            "macro_precision": sum(macro_precisions) / len(macro_precisions) if macro_precisions else 0.0
        }

    def calculate_recall(self, k: Optional[int] = None) -> Dict[str, float]:
        """
        검색된 문서의 재현율을 계산합니다.

        Args:
            k (Optional[int], optional): 고려할 상위 문서 수. 기본값은 None

        Returns:
            Dict[str, float]: 재현율 딕셔너리
        """

        micro_recall = 0
        macro_recalls = []

        for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs):
            relevant_count = sum(
                1 for actual_doc in actual_docs
                if any(self.text_match(actual_doc.page_content, pred_doc.page_content) for pred_doc in predicted_docs[:k])
            )
            micro_recall += relevant_count
            macro_recalls.append(relevant_count / len(actual_docs) if actual_docs else 0)

        total_actual = sum(len(actual_docs) for actual_docs in self.actual_docs)
        

        return {
            "micro_recall": micro_recall / total_actual if total_actual > 0 else 0.0,
            "macro_recall": sum(macro_recalls) / len(macro_recalls) if macro_recalls else 0.0
        }
    

    def calculate_f1_score(self, k: Optional[int] = None) -> Dict[str, float]:
        """
        검색된 문서의 F1 점수를 계산합니다.

        Args:
            k (Optional[int], optional): 고려할 상위 문서 수. 기본값은 None

        Returns:
            Dict[str, float]: F1 점수 딕셔너리
        """
        precision = self.calculate_precision(k)
        recall = self.calculate_recall(k)

        micro_f1 = 2 * (precision['micro_precision'] * recall['micro_recall']) / (precision['micro_precision'] + recall['micro_recall']) if (precision['micro_precision'] + recall['micro_recall']) > 0 else 0.0
        macro_f1 = 2 * (precision['macro_precision'] * recall['macro_recall']) / (precision['macro_precision'] + recall['macro_recall']) if (precision['macro_precision'] + recall['macro_recall']) > 0 else 0.0

        return {
            "micro_f1": micro_f1,
            "macro_f1": macro_f1
        }

    def calculate_mrr(self, k: Optional[int] = None) -> Dict[str, float]:
        """
        평균 역순위(Mean Reciprocal Rank, MRR)를 계산합니다.

        Args:
            k (Optional[int], optional): 고려할 상위 문서 수. 기본값은 None

        Returns:
            Dict[str, float]: MRR 점수 딕셔너리
        """
        reciprocal_ranks = []
        for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs):
            for rank, pred_doc in enumerate(predicted_docs[:k], start=1):
                if any(self.text_match(actual_doc.page_content, pred_doc.page_content) for actual_doc in actual_docs):
                    reciprocal_ranks.append(1 / rank)
                    break
            else:
                reciprocal_ranks.append(0)
        
        mrr = sum(reciprocal_ranks) / len(reciprocal_ranks) if reciprocal_ranks else 0.0
        return {"mrr": mrr}

    def calculate_map(self, k: Optional[int] = None) -> Dict[str, float]:
        """
        평균 정확도(Mean Average Precision, MAP)를 계산합니다.

        Args:
            k (Optional[int], optional): 고려할 상위 문서 수. 기본값은 None

        Returns:
            Dict[str, float]: MAP 점수 딕셔너리
        """

        average_precisions = []
        for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs):
            relevant_docs = 0
            precision_sum = 0
            for i, pred_doc in enumerate(predicted_docs[:k], start=1):
                if any(self.text_match(actual_doc.page_content, pred_doc.page_content) for actual_doc in actual_docs):
                    relevant_docs += 1
                    precision_sum += relevant_docs / i
            average_precision = precision_sum / len(actual_docs) if actual_docs else 0
            average_precisions.append(average_precision)
        
        map_score = sum(average_precisions) / len(average_precisions) if average_precisions else 0.0
        return {"map": map_score}


    def calculate_ndcg(self, k: Optional[int] = None) -> Dict[str, float]:
        """
        정규화된 할인 누적 이득(Normalized Discounted Cumulative Gain, NDCG)을 계산합니다.

        Args:
            k (Optional[int], optional): 고려할 상위 문서 수. 기본값은 None

        Returns:
            Dict[str, float]: NDCG 점수 딕셔너리
        """
        def dcg(relevances):
            return sum((2**rel - 1) / math.log2(i + 2) for i, rel in enumerate(relevances[:k]))

        ndcg_scores = []
        for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs):
            relevances = [
                1 if any(self.text_match(actual_doc.page_content, pred_doc.page_content) for actual_doc in actual_docs) else 0
                for pred_doc in predicted_docs[:k]
            ]
            ideal_relevances = sorted(relevances, reverse=True)
            
            dcg_score = dcg(relevances)
            idcg_score = dcg(ideal_relevances)
            
            ndcg_scores.append(dcg_score / idcg_score if idcg_score > 0 else 0)
        
        ndcg = sum(ndcg_scores) / len(ndcg_scores) if ndcg_scores else 0.0
        return {"ndcg": ndcg}


    def visualize_results(self, k: Optional[int] = None):
        """
        평가 결과를 시각화합니다.

        Args:
            k (Optional[int], optional): 고려할 상위 문서 수. 기본값은 None
        """
        metrics = {
            "Precision": self.calculate_precision,
            "Recall": self.calculate_recall,
            "F1 Score": self.calculate_f1_score,
            "NDCG": self.calculate_ndcg,
            "Hit Rate": self.calculate_hit_rate,
            "MRR": self.calculate_mrr,
            "MAP": self.calculate_map
        }

        results = {name: func(k) for name, func in metrics.items()}

        plt.figure(figsize=(12, 6))
        x = range(len(metrics))
        
        for i, (name, result) in enumerate(results.items()):
            values = list(result.values())
            if len(values) == 1:
                plt.bar(i, values[0], 0.4, label=name, alpha=0.6)
            else:
                plt.bar(i - 0.2, values[0], 0.4, label=f'{name} (Micro)', color='blue', alpha=0.6)
                plt.bar(i + 0.2, values[1], 0.4, label=f'{name} (Macro)', color='red', alpha=0.6)

        plt.xlabel('Metrics')
        plt.ylabel('Score')
        plt.title(f'Evaluation Results (k={k if k else "all"})')
        plt.xticks(x, list(metrics.keys()), rotation=45, ha='right')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()  



class RougeOfflineRetrievalEvaluators(OfflineRetrievalEvaluators):
    def __init__(self, actual_docs: List[List[Document]], predicted_docs: List[List[Document]], 
                 match_method: str = "rouge1", averaging_method: AveragingMethod = AveragingMethod.BOTH, 
                 matching_criteria: MatchingCriteria = MatchingCriteria.ALL, threshold: float = 0.5) -> None:
        """
        RougeOfflineRetrievalEvaluators 클래스를 초기화합니다.

        Args:
            actual_docs (List[List[Document]]): 실제 문서 리스트의 리스트
            predicted_docs (List[List[Document]]): 예측된 문서 리스트의 리스트
            match_method (str, optional): 문서 매칭을 위한 ROUGE 방법. 기본값은 "rouge1"
            averaging_method (AveragingMethod, optional): 결과 평균 계산 방법. 기본값은 AveragingMethod.BOTH
            matching_criteria (MatchingCriteria, optional): 히트로 간주할 기준. 기본값은 MatchingCriteria.ALL
            threshold (float, optional): ROUGE 점수 임계값. 기본값은 0.5
        """
        super().__init__(actual_docs, predicted_docs, match_method, averaging_method, matching_criteria)
        self.threshold = threshold
        self.scorer = rouge_scorer.RougeScorer([match_method], use_stemmer=True)
    
    @lru_cache(maxsize=1000)
    def text_match(self, actual_text: str, predicted_text: Union[str, List[str]]) -> bool:
        """
        ROUGE 점수를 사용하여 실제 텍스트가 예측 텍스트와 일치하는지 확인합니다.

        Args:
            actual_text (str): 실제 텍스트
            predicted_text (Union[str, List[str]]): 예측 텍스트 또는 텍스트 리스트

        Returns:
            bool: 일치하면 True, 그렇지 않으면 False
        """

        # Kiwi 형태소 분석기를 사용하여 토큰화 (기본 토크나이저가 띄어쓰기 기준이라서)
        kiwi = Kiwi()
        actual_tokens = [t.form for t in kiwi.tokenize(actual_text)]
        actual_text = " ".join(actual_tokens)


        if self.match_method in ["rouge1", "rouge2", "rougeL"]:
            if isinstance(predicted_text, list):
                new_predicted_text = []
                for text in predicted_text:
                    prediction_tokens = [t.form for t in kiwi.tokenize(text)]
                    new_predicted_text.append(" ".join(prediction_tokens))

                return any(self.scorer.score(actual_text, text)[self.match_method].fmeasure >= self.threshold for text in new_predicted_text)
            else:
                prediction_tokens = [t.form for t in kiwi.tokenize(predicted_text)]
                predicted_text = " ".join(prediction_tokens)
                score = self.scorer.score(actual_text, predicted_text)[self.match_method].fmeasure
                return score >= self.threshold
        else:
            return super().text_match(actual_text, predicted_text)

    def calculate_ndcg(self, k: Optional[int] = None) -> Dict[str, float]:
        """
        ROUGE 점수를 사용하여 정규화된 할인 누적 이득(Normalized Discounted Cumulative Gain, NDCG)을 계산합니다.

        Args:
            k (Optional[int], optional): 고려할 상위 문서 수. 기본값은 None

        Returns:
            Dict[str, float]: NDCG 점수 딕셔너리
        """
        def dcg(relevances):
            return sum((2**rel - 1) / math.log2(i + 2) for i, rel in enumerate(relevances[:k]))

        ndcg_scores = []
        for actual_docs, predicted_docs in zip(self.actual_docs, self.predicted_docs):
            relevances = [
                max(self.scorer.score(actual_doc.page_content, pred_doc.page_content)[self.match_method].fmeasure 
                    for actual_doc in actual_docs)
                for pred_doc in predicted_docs[:k]
            ]
            ideal_relevances = sorted(relevances, reverse=True)
            
            dcg_score = dcg(relevances)
            idcg_score = dcg(ideal_relevances)
            
            ndcg_scores.append(dcg_score / idcg_score if idcg_score > 0 else 0)
        
        ndcg = sum(ndcg_scores) / len(ndcg_scores) if ndcg_scores else 0.0
        return {"ndcg": ndcg}
