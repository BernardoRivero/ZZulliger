#from actions.actions import imprimirSlot
#import json
from typing import Any, List, Dict, Text, Optional

from rasa.core.featurizers.tracker_featurizers import TrackerFeaturizer
from rasa.core.policies.policy import PolicyPrediction, confidence_scores_for, \
    Policy
from rasa.shared.core.domain import Domain
from rasa.shared.core.generator import TrackerWithCachedStates
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.shared.nlu.interpreter import NaturalLanguageInterpreter
from rasa.utils.endpoints import *
from typing import Any, Text, Dict, List
#from rasa_sdk import Action, Tracker
#from rasa_sdk import imprimirSlot
from rasa_sdk.executor import CollectingDispatcher
#from rasa_sdk.events import SlotSet,AllSlotsReset


class TestPolicy(Policy):

    def __init__(
            self,
            featurizer: Optional[TrackerFeaturizer] = None,
            priority: int = 2,
            should_finetune: bool = False,
            **kwargs: Any
    ) -> None:
        super().__init__(featurizer, priority, should_finetune, **kwargs)
        self._contador = 0
        self._respuesta1 = ""
        self._respuesta2 = ""
        self._respuesta3 = ""
        

    def train(
            self,
            training_trackers: List[TrackerWithCachedStates],
            domain: Domain,
            interpreter: NaturalLanguageInterpreter,
            **kwargs: Any
    ) -> None:
        pass

    def predict_action_probabilities(
            self, 
            tracker: DialogueStateTracker,
            domain: Domain,
            interpreter: NaturalLanguageInterpreter,
            **kwargs: Any
            
    ) -> "PolicyPrediction":
        intent = tracker.latest_message.intent

        # If the last thing rasa did was listen to a user message, we need to
        # send back a response.
        if tracker.latest_action_name == "action_listen":
            # The user starts the conversation.
            if intent["name"] == "respuestas":
                self._contador = self._contador + 1
                if self._contador == 1:
                    self._respuesta1 = tracker
                else:
                    if self._contador == 2:
                        self._respuesta2 = tracker
                    else:
                        if self._contador == 3:
                            self._respuesta3 = tracker
                print(self._contador)
                if self._contador < 4:
                    return[self._prediction(confidence_scores_for("action_imprimir_slot", 1.0, domain))]
        # If rasa latest action isn't "action_listen", it means the last thing
        # rasa did was send a response, so now we need to listen again so the
        # user can talk to us.
        print(self._contador)
        return self._prediction(confidence_scores_for(
            "action_listen", 1.0, domain
        ))

    def _metadata(self) -> Dict[Text, Any]:
        return {
            "priority": 2
        }

    @classmethod
    def _metadata_filename(cls) -> Text:
        return "test_policy.json"