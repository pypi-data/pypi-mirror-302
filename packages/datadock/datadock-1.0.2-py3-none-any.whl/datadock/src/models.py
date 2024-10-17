# import re
# import spacy
# from typing import Tuple, List, Any, Optional, Union
# from transformers import (
#     AutoTokenizer,
#     AutoModelForSeq2SeqLM,
#     AutoModelForTokenClassification,
#     BartTokenizer,
#     BartForConditionalGeneration,
#     BertForTokenClassification,
#     pipeline,
#     PreTrainedModel,
#     BatchEncoding,
# )
#
#
# def check_text(text):
#     # List of phrases to check for
#     invalid_phrases = ["None.", "Not applicable."]
#     cleaned_text = text.strip()
#     # Check if any invalid phrase is in the text
#     if any(phrase in cleaned_text for phrase in invalid_phrases):
#         return "No text"
#
#     pattern = r"\b(\w+)[.-](\w+)\b(?!\stv[A-Z])"
#     modified_text = re.sub(pattern, r"\1\2", cleaned_text)
#
#     # Otherwise, return the original text
#     return modified_text
#
#
# class TextSummaryModel:
#     """
#     A class for text summarization using a pre-trained BART (Bidirectional AutoRegressive Transformer) model.
#
#     This class handles the initialization of the BART model and tokenizer,
#     as well as chunking the input text when necessary, to generate summaries for both small and large texts.
#     """
#
#     def __init__(self) -> None:
#         """
#         Initializes the TextSummaryModel instance by loading the pre-trained BART model and tokenizer.
#         """
#         self._tokenizer, self._model = self._initialize_model()
#
#     @classmethod
#     def _initialize_model(cls) -> Tuple[BartTokenizer, PreTrainedModel]:
#         """
#         Initializes the pre-trained BART model and tokenizer for text summarization.
#
#         Returns:
#             A tuple containing the initialized BartTokenizer and BartForConditionalGeneration model.
#         """
#         summary_model_name = "facebook/bart-large-cnn"
#         summary_tokenizer = BartTokenizer.from_pretrained(summary_model_name)
#         summary_model = BartForConditionalGeneration.from_pretrained(summary_model_name)
#         return summary_tokenizer, summary_model
#
#     def _chunk_text(
#         self, text: str, chunk_size: int = 1024, overlap: int = 100
#     ) -> list:
#         """
#         Splits the input text into overlapping chunks based on the specified chunk size and overlap.
#
#         Parameters:
#             text (str): The input text to be chunked.
#             chunk_size (int): The size of each chunk. Default is 1024 tokens.
#             overlap (int): The overlap between adjacent chunks to ensure continuity. Default is 100 tokens.
#
#         Returns:
#             list: A list of tokenized chunks.
#         """
#         text_token = self._tokenizer(text, return_tensors="pt", truncation=False)
#         input_ids = text_token["input_ids"][0]
#
#         # create overlapping chunks
#         chunks = [
#             input_ids[i : i + chunk_size]
#             for i in range(0, len(input_ids), chunk_size - overlap)
#         ]
#         return chunks
#
#     def summarize(
#         self,
#         text: str,
#         chunk_size: int = 1024,
#         overlap: int = 100,
#         threshold: int = 1024,
#     ) -> Optional[str]:
#         """
#         Generates a summary for the input text. Handles small texts without chunking and large texts with chunking.
#
#         Parameters:
#             text (str): The input text to be summarized.
#             chunk_size (int): The size of each chunk for large texts. Default is 1024 tokens.
#             overlap (int): The overlap between adjacent chunks for large texts. Default is 100 tokens.
#             threshold (int): The token length above which chunking will be applied. Default is 1024 tokens.
#
#         Returns:
#             str: The final summarized text.
#         """
#         cleaned_text = check_text(text)
#
#         if cleaned_text == "No text":
#             return "No text for analysis"
#
#         input_token = self._tokenizer(
#             cleaned_text, return_tensors="pt", truncation=False
#         )
#         input_ids_length = input_token["input_ids"].shape[1]
#
#         if input_ids_length <= threshold:
#             return self._generate_summary(input_token["input_ids"][0])
#
#         chunks = self._chunk_text(cleaned_text, chunk_size, overlap)
#         summaries = [self._generate_summary(chunk) for chunk in chunks]
#         return " ".join(summaries)
#
#     def _generate_summary(self, input_ids: BatchEncoding) -> str:
#         """
#         Generates a summary from the tokenized input IDs using the pre-trained BART model.
#
#         Parameters:
#             input_ids (BatchEncoding): The tokenized input IDs.
#
#         Returns:
#             str: The generated summary text.
#         """
#         summary_ids = self._model.generate(
#             input_ids.unsqueeze(0),
#             max_length=150,
#             min_length=40,
#             length_penalty=2.0,
#             num_beams=4,
#             early_stopping=True,
#         )
#         return self._tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#
#
# class SentimentAnalysisModel:
#     """
#     The `SentimentAnalysisModel` class is designed to perform sentiment analysis on input
#     text using a pre-trained
#     DistilBERT model fine-tuned for sentiment analysis. The class includes functionalities to
#     handle both small and large texts, chunking the text as needed for efficient analysis.
#     """
#
#     def __init__(self) -> None:
#         """
#         Constructor method that initializes the sentiment analysis pipeline using a pre-trained model.
#
#         Returns:
#             None
#         """
#         self._sentiment_pipeline = self._initialize_model()
#
#     @classmethod
#     def _initialize_model(cls) -> pipeline:
#         """
#         Initializes the sentiment analysis model using a pre-trained DistilBERT model fine-tuned
#         for sentiment analysis.
#
#         Returns:
#             pipeline: A Hugging Face pipeline object configured for sentiment analysis.
#
#         Model Details:
#             - Model Name: `distilbert-base-uncased-finetuned-sst-2-english`
#             - The model is fine-tuned to classify text as either positive or negative.
#         """
#         # Sentiment Analysis model
#         sentiment_model_name = "distilbert-base-uncased-finetuned-sst-2-english"
#         return pipeline("sentiment-analysis", model=sentiment_model_name)
#
#     @staticmethod
#     def _chunk_text(text: str, chunk_size: int = 512) -> list:
#         """
#         Splits the input text into smaller chunks of a specified size.
#
#         Parameters:
#             text (str): The input text to be chunked.
#             chunk_size (int): The size of each chunk. Default is 512.
#
#         Returns:
#             chunks (list): A list of text chunks.
#         """
#         return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]
#
#     def sentiment_analysis(
#         self, text: str, chunk_size: int = 512
#     ) -> Optional[Union[Tuple[Any, Any], str]]:
#         """
#         Analyzes the sentiment of the input text. If the text is small (i.e., less than or equal to the chunk size),
#         it processes the text in one go. If the text is large, it splits the text into chunks and
#         analyzes each chunk separately.
#
#         Parameters:
#             text (str): The input text to be analyzed.
#             chunk_size (int): The size of each chunk for large texts. Default is 512.
#
#         Returns:
#             Tuple containing:
#             - Negative scores (float or list): Sentiment score(s) indicating the negative sentiment in the text.
#             - Positive scores (float or list): Sentiment score(s) indicating the positive sentiment in the text.
#         """
#         cleaned_text = check_text(text)
#
#         if cleaned_text == "No text":
#             return "No text for analysis"
#
#         if len(cleaned_text) <= chunk_size:
#             return self._analyze_single_chunk(cleaned_text)
#
#         chunks = self._chunk_text(cleaned_text, chunk_size)
#         return self._analyze_chunks(chunks)
#
#     def _analyze_single_chunk(self, text: str) -> Tuple[float, float]:
#         """
#         Analyzes the sentiment of a single chunk of text.
#
#         Parameters:
#             text (str): The input text chunk to be analyzed.
#
#         Returns:
#             Tuple containing:
#             - Negative score (float): The sentiment score indicating the negative sentiment in the chunk.
#             - Positive score (float): The sentiment score indicating the positive sentiment in the chunk.
#         """
#         result = self._sentiment_pipeline(text)
#         negative_score = (
#             round(result[0]["score"], 2) if result[0]["label"] == "NEGATIVE" else 0.0
#         )
#         positive_score = (
#             round(result[0]["score"], 2) if result[0]["label"] == "POSITIVE" else 0.0
#         )
#         return negative_score, positive_score
#
#     def _analyze_chunks(self, chunks: list) -> Tuple[list, list]:
#         """
#         Analyzes the sentiment of each chunk in a list of text chunks.
#
#         Parameters:
#             chunks (list): A list of text chunks to be analyzed.
#
#         Returns:
#             Tuple containing:
#             - negative_scores (list): A list of sentiment scores indicating the negative sentiment in each chunk.
#             - positive_scores (list): A list of sentiment scores indicating the positive sentiment in each chunk.
#         """
#         negative_scores = []
#         positive_scores = []
#
#         for chunk in chunks:
#             negative_score, positive_score = self._analyze_single_chunk(chunk)
#             if negative_score:
#                 negative_scores.append(negative_score)
#             if positive_score:
#                 positive_scores.append(positive_score)
#         return negative_scores, positive_scores
#
#
# class EntityRecognitionModel:
#     """
#     The `EntityRecognitionModel` class is designed to perform entity recognition on input text using a
#     pre-trained BERT model fine-tuned for the CoNLL-2003 dataset. The class encapsulates the model initialization,
#     text preprocessing, and entity extraction functionalities.
#     """
#
#     def __init__(self) -> None:
#         """
#         Constructor method that initializes the entity recognition pipeline by loading
#         the pre-trained model and tokenizer.
#
#         Returns:
#             None
#         """
#         self._ner_pipeline = self._initialize_model()
#         self._nlp = spacy.load("en_core_web_sm")
#
#     @classmethod
#     def _initialize_model(cls) -> pipeline:
#         """
#         Initializes the entity recognition model using a pre-trained BERT model fine-tuned for the CoNLL-2003 dataset.
#         Sets up the Hugging Face pipeline with the model and tokenizer.
#
#         Returns:
#             pipeline: A Hugging Face pipeline object configured for Named Entity Recognition (NER).
#
#         Model Details:
#             - Model Name: `dbmdz/bert-large-cased-finetuned-conll03-english`
#             - The model is fine-tuned for entity recognition tasks and returns grouped entities.
#         """
#         # Entity Model
#         entity_model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"
#
#         entity_tokenizer = AutoTokenizer.from_pretrained(entity_model_name)
#         entity_model = BertForTokenClassification.from_pretrained(entity_model_name)
#         return pipeline(
#             "ner", model=entity_model, tokenizer=entity_tokenizer, grouped_entities=True
#         )
#
#     def entity_recognition(self, text: str) -> Optional[Union[List[str], str]]:
#         """
#         Performs entity recognition on the given text. First preprocesses the text and then applies the
#         NER pipeline to extract recognized entities.
#
#         Parameters:
#             text (str): The input text to be analyzed for entity recognition.
#
#         Returns:
#             entities (List[str]): A list of recognized entities from the input text.
#         """
#         cleaned_text = check_text(text)
#
#         if cleaned_text == "No text":
#             return "No text for analysis"
#
#         hf_entities = self._ner_pipeline(cleaned_text)
#         # spacy_entities = self._nlp(cleaned_text)
#         # sp_entities = [{"word": entity.text, "entity": entity.label_} for entity in spacy_entities.ents]
#
#         combined_entities = hf_entities
#         return [entity["word"] for entity in combined_entities]
