from networksecurity.logging.logger import logging
from networksecurity.exception.exception import CustomException
from networksecurity.entity.artifact_entity import ModelTrainerArtifact,ClassificationMetricsArtifact
from sklearn.metrics import f1_score,precision_score,recall_score

def get_classification_score(y_true,y_pred)->ClassificationMetricsArtifact:
    try:

        model_fi_score=f1_score(y_true,y_pred)
        model_precision_score=precision_score(y_true,y_pred)
        model_recall_score=recall_score(y_true,y_pred)

        clssification_report=ClassificationMetricsArtifact(
            f1_score=model_fi_score,
            precision_score=model_precision_score,
            recall_score=model_recall_score
        )
        logging.info(f'Model Classification report: {clssification_report}')
        return clssification_report
    except Exception as e:
        raise CustomException(e,SyntaxError)