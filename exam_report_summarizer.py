# Designed by Prakash Srinivasan ( prarvy@gmail.com )
# Project Name: Report Summarizer
# Version: 1.0: Base version by author

import csv


class CSVDataReader:
    def __init__(self):
        self.report = {}
        self.data = None
        self.field_names = ['Exam Name', 'Number of Candidates', 'Number of Passed Exams', 'Number of Failed Exams',
                            'Best Score', 'Worst Score']

    def csv_file_reader(self, filename):
        with open(filename, 'r') as input_file:
            self.data = list(csv.DictReader(input_file, delimiter=','))

    def report_processor(self):
        for data in self.data:
            exam_name = data['Exam Name']
            candidate = data['Candidate ID']
            score = float(data['Score'])
            grade = data['Grade']
            if exam_name not in self.report:
                self.report[exam_name] = {
                    'candidates': set(),
                    'number_of_passed_exams': 0,
                    'number_of_failed_exams': 0,
                    'best_score': float('-inf'),
                    'worst_score': float('inf'),
                }
            self.report[exam_name]['candidates'].add(candidate)
            if grade == 'Pass':
                self.report[exam_name]['number_of_passed_exams'] += 1
            else:
                self.report[exam_name]['number_of_failed_exams'] += 1
            self.report[exam_name]['best_score'] = max(score, float(self.report[exam_name]['best_score']))
            self.report[exam_name]['worst_score'] = min(score, float(self.report[exam_name]['worst_score']))

    def export_report(self, report_name):
        with open(report_name, 'w', newline='') as file:

            writer = csv.DictWriter(file, fieldnames=self.field_names)
            writer.writeheader()

            for exam_name, exam_data in self.report.items():
                writer.writerow({
                    'Exam Name': exam_name,
                    'Number of Candidates': len(exam_data['candidates']),
                    'Number of Passed Exams': exam_data['number_of_passed_exams'],
                    'Number of Failed Exams': exam_data['number_of_failed_exams'],
                    'Best Score': int(exam_data['best_score']),
                    'Worst Score': int(exam_data['worst_score'])
                })

        print('Report Name:', report_name, 'has been generated successfully.\nPreview of the report is printed below.')

        with open(report_name, 'r') as report_file:
            reports = csv.reader(report_file)
            for data in list(reports):
                print(data)


if __name__ == '__main__':
    reader = CSVDataReader()
    reader.csv_file_reader('exam_results.csv')
    reader.report_processor()
    reader.export_report('summary_report.csv')
