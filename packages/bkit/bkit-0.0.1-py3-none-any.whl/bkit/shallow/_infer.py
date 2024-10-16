import os
from typing import List, Union

import gdown
import torch

import bkit
from bkit.pos import Infer as PosInfer
from bkit.shallow._models import decoder
from bkit.utils import MODEL_URL_MAP


def get_model_object():
    """
    Download and load the pre-trained model.

    Returns:
        model_object: Loaded pre-trained model.
    """
    url = MODEL_URL_MAP["shallow"]
    cache_dir = bkit.ML_MODELS_CACHE_DIR
    model_path = os.path.join(cache_dir, "shallow_model.pt")

    # Create the cache directory if it doesn't exist
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    # Download the model if it doesn't exist in the cache
    if not os.path.exists(model_path):
        gdown.download(url, model_path, quiet=False, fuzzy=True)

    # Load the model using torch_load from utils
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_object = torch.load(model_path, map_location=device)

    return model_object


class Infer(object):
    def __init__(self, pos_model: str = "pos-noisy-label", batch_size: int = 1):
        """
        Initialize a ShallowInference instance.

        Args:
            batch_size (int, optional): The batch size for inference. Defaults to 1.
        """

        # Obtain the pre-trained model object
        self.model_object = get_model_object()

        # Extract model specifications and state dictionary
        self.model_spec = self.model_object["spec"]
        self.model_state_dict = self.model_object["state_dict"]

        # Create a chart parser model using the specifications and state dictionary
        self.model = decoder.ChartParser.from_spec(
            self.model_spec, self.model_state_dict
        )

        # Initialize a part-of-speech tagging model
        self.pos_model = PosInfer(pos_model)

        # Set the batch size for inference
        self.batch_size = batch_size

    def __call__(self, text: Union[str, List[str]]) -> Union[str, List[str]]:
        """
        Perform shallow inference on the provided input text or list of texts.

        Args:
            text (Union[str, List[str]]): Input text or list of texts for shallow inference.

        Returns:
            Union[str, List[str]]: Inference results as a single string or a list of strings.
        """

        # Get sentences and corresponding part-of-speech tags for the input text
        sentences, tags = self.get_sentences_with_tags(text)

        all_predicted = []
        for start_index in range(0, len(sentences), self.batch_size):
            subbatch_sentences = sentences[start_index : start_index + self.batch_size]

            subbatch_tags = tags[start_index : start_index + self.batch_size]
            subbatch_sentences = [
                [(tag, word) for tag, word in zip(taag, sentence)]
                for taag, sentence in zip(subbatch_tags, subbatch_sentences)
            ]

            predicted, _ = self.model.parse_batch(subbatch_sentences)
            del _

            all_predicted.extend([p.convert() for p in predicted])

        if len(all_predicted) == 1:
            return all_predicted[0].linearize()
        else:
            return [predicted.linearize() for predicted in all_predicted]

    def get_pos_tag(self, sentence):
        """
        Perform part-of-speech tagging on a sentence and return the list of POS tags.

        Args:
            sentence (str): Input sentence for part-of-speech tagging.

        Returns:
            List[str]: List of part-of-speech tags for words in the sentence.
        """
        pos_tagger_results = self.pos_model(sentence)

        poses = []
        for word, pos, confidence in pos_tagger_results:
            poses.append(pos)
        return poses

    def get_sentences_with_tags(
        self, text: Union[str, List[str]]
    ) -> Union[str, List[str]]:
        """
        Tokenize input text or list of texts and perform part-of-speech tagging on each sentence.

        Args:
            text (Union[str, List[str]]): Input text or list of texts.

        Returns:
            Tuple[List[List[str]], List[List[str]]]: Lists of tokenized sentences and their corresponding POS tags.
        """
        if isinstance(text, str):
            raw_sentences = [text]

        elif isinstance(text, list):
            raw_sentences = text

        else:
            raise ValueError("Invalid input! \n Give a string or a list of strings.")

        sentences = []
        tags = []
        for sentence in raw_sentences:
            sentences.append(bkit.tokenizer.tokenize(sentence))
            tags.append(self.get_pos_tag(sentence))

        return sentences, tags
