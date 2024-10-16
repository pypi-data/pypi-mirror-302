from .PgsFile import PGScraper
from .PgsFile import audiovisual_downloader

from .PgsFile import install_package, uninstall_package
from .PgsFile import run_script, run_command

from .PgsFile import get_data_text, get_data_lines, get_json_lines, get_tsv_lines
from .PgsFile import get_data_excel, get_data_json, get_data_tsv, extract_misspelled_words_from_docx

from .PgsFile import write_to_txt, write_to_excel, write_to_json, write_to_json_lines

from .PgsFile import FilePath, FileName, makedirec, get_subfolder_path, get_package_path, DirList
from .PgsFile import source_path, next_folder_names, corpus_root, get_directory_tree_with_meta, find_txt_files_with_keyword
from .PgsFile import remove_empty_folders, remove_empty_txts, remove_empty_lines, remove_empty_last_line

from .PgsFile import BigPunctuation, StopTags, Special
from .PgsFile import ZhStopWords, EnPunctuation, extract_stopwords
from .PgsFile import nltk_en_tags, nltk_tag_mapping, thulac_tags, ICTCLAS2008

from .PgsFile import ngrams, bigrams, trigrams, everygrams
from .PgsFile import word_list, batch_word_list
from .PgsFile import cs, cs1, cs2

from .PgsFile import strQ2B_raw, strQ2B_words, Percentage, decimal_to_percent, get_text_length_kb, extract_numbers
from .PgsFile import check_contain_chinese, check_contain_number
from .PgsFile import replace_chinese_punctuation_with_english
from .PgsFile import replace_english_punctuation_with_chinese
from .PgsFile import clean_list, yhd, extract_chinese_punctuation, generate_password, sort_strings_with_embedded_numbers

name = "PgsFile"