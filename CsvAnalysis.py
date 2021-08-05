import csv
import glob


class Analysis:
    """Class created to analyze text files
    based on information obtained from a properly prepared list in a csv file"""

    def __init__(self, main_path, data_path):
        """Initialization function in which it declares all variables used by later functions """
        self.list_of_fails = []
        self.rows_details = {}
        self.list_of_excel_rows = []
        self.main_path = main_path
        self.data_path = data_path
        self.reader = csv.reader(open(main_path))
        self.list_of_files = glob.glob(f'{data_path}/*')
        self.final_list_of_sentences = []
        self.sentence_count = 0
        # prepare a list of row contents from a specified csv file
        for row in self.reader:
            self.list_of_excel_rows.append(row)
        self.paragraph_count = 0
        self.average_char_for_par = 0
        self.average_number_of_sentences_in_par = 0
        self.punctation_marks_count = 0
        self.average_number_of_words_in_par = 0
        self.count_char = 0

    def get_path(self, excel_row):
        """ function is responsible for selecting a path to a txt file
         based on data from a csv row. """
        if len(excel_row) == 2:
            print(excel_row[0])
            if int(excel_row[0]) > 10:
                # checking if a text file is prepared for the given number
                for file in self.list_of_files:
                    if excel_row[0] in file:
                        path = file
                        return path
            else:
                path = f"{self.data_path}/{excel_row[1]}"
                return path

    def current_row(self, excel_row):
        """ This function is responsible for opening the text file
        based on the path found in the get_path function """
        path = self.get_path(excel_row)
        text_file = open(path)
        text_reader_in_list = text_file.readlines()
        return text_reader_in_list

    def text_unification(self, excel_row):
        """ This function is responsible for unifying a text file
         opened from current_row function into one string """
        text_reader_in_list = self.current_row(excel_row)
        text_united = ' '.join([str(n) for n in text_reader_in_list])
        return text_united

    def count_paragraphs(self, excel_row):
        """ This function is responsible for counting paragraphs on
        text file opened with current_row function"""
        text_reader_in_list = self.current_row(excel_row)
        self.paragraph_count = 0
        for i in range(len(text_reader_in_list)):
            if len(text_reader_in_list[i]) > 1:
                self.paragraph_count += 1

    def count_sentences(self, excel_row):
        """ This function is responsible for counting sentences
         in text file presented as one string from function text_unification"""
        text_united = self.text_unification(excel_row)
        list_of_sentences = text_united.split(".")
        for sentence in list_of_sentences:
            if len(sentence) > 2:
                self.final_list_of_sentences.append(sentence)
        self.sentence_count = len(self.final_list_of_sentences)

    def characters_avrg(self, excel_row):
        """ This function is responsible for counting characters and
        counting average number of characters in paragraph
         based on the text from text_unification function """
        text_united = self.text_unification(excel_row)
        self.count_char = len(text_united)
        self.average_char_for_par = self.count_char / self.paragraph_count

    def avrg_sent_par(self):
        """ This function is responsible for counting
         average number of sentences in text based on
          result of count_sentences function """
        self.average_number_of_sentences_in_par = self.sentence_count \
                                                  / self.paragraph_count

    def count_punc_marks(self, excel_row):
        """ This function is responsible for counting punctuation marks
        based on the text from text_unification function """
        text_united = self.text_unification(excel_row)
        punctation_marks_count_quotes = text_united.count('"') +\
                                        text_united.count("'")
        punctation_marks_ellipsis = text_united.count('...')
        self.punctation_marks_count = (text_united.count(".") -
                                       punctation_marks_ellipsis * 3) \
                                      + text_united.count(";") \
                                      + text_united.count(",") \
                                      + text_united.count(":") \
                                      + text_united.count("-") \
                                      + text_united.count("?") \
                                      + text_united.count("!") \
                                      + text_united.count("(") \
                                      + int(punctation_marks_count_quotes / 2) \
                                      + punctation_marks_ellipsis

    def avrg_word_par(self, excel_row):
        """ This function is responsible for counting
        the average number of words in a paragraph
        based on text from text_unification function """
        text_united = self.text_unification(excel_row)
        list_of_words = text_united.split(" ")
        self.average_number_of_words_in_par = len(list_of_words) / self.paragraph_count

    def save(self, excel_row):
        """This function is responsible for storing
        the actual values of the variables in the dict for later use """
        self.rows_details[f'Row{excel_row[0]}'] = {"lp": excel_row[0],
                                                   "file": excel_row[1],
                                                   "paragraph_count": self.paragraph_count,
                                                   "sentence_count": self.sentence_count,
                                                   "average_number_of_sentences_in_par":
                                                       self.average_number_of_sentences_in_par,
                                                   "count_char": self.count_char,
                                                   "average_char_for_par": self.average_char_for_par,
                                                   "punctation_marks_count": self.punctation_marks_count,
                                                   "average_number_of_words_in_par": self.average_number_of_words_in_par}

    def csv_save(self, save_file_name):
        """ This function is responsible for saving results as csv
        based on dict used in save function """
        # CSV Save
        csv_file_output = open(f'{save_file_name}.csv', "w", newline="")
        column_names = list(self.rows_details["Row0"].keys())
        csv_writer = csv.DictWriter(csv_file_output, fieldnames=column_names)
        csv_writer.writeheader()
        del self.rows_details["Rowlp"]
        for key in self.rows_details:
            csv_writer.writerow(self.rows_details[f'{key}'])

    def entire_analysis(self):
        """ This function is responsible for running
        all the functions needed to satisfy the assumptions from the task.txt file """
        for row in self.list_of_excel_rows:
            try:
                self.count_paragraphs(row)
                self.count_sentences(row)
                self.characters_avrg(row)
                self.avrg_sent_par()
                self.count_punc_marks(row)
                self.avrg_word_par(row)
                self.save(row)
            except:
                self.list_of_fails.append(row)
                self.rows_details[f'Row{row[0]}'] = {"lp": row[0],
                                                     "file": "no such file",
                                                     "paragraph_count": 0,
                                                     "sentence_count": 0,
                                                     "average_number_of_sentences_in_par": 0,
                                                     "count_char": 0,
                                                     "average_char_for_par": 0,
                                                     "punctation_marks_count": 0,
                                                     "average_number_of_words_in_par": 0}
        self.csv_save("results")


Analysis('texts.csv', 'data').entire_analysis()
