from collections import OrderedDict
import typing

if not __package__:
    from parser import BaseParser, BasicParser
else:
    from .parser import BaseParser, BasicParser


class DataFormatter:
    """
    To add support for new data formats, simply implement the method,
    and include its name in self._formats along with the corresponding method
    name.
    """

    def __init__(self, format: str, data: dict):
        self.data = data
        self.format = format
        self._formats = {
            'json': self.as_json,
            'csv': self.as_csv
        }

    def output(self):
        try:
            return self._formats[self.format]()
        except KeyError:
            return {'details': f'Unsupported format: {self.format}'}

    def as_json(self):
        import json
        return json.dumps(self.data)

    def as_csv(self):
        return 'Not Implemented'


class BaseCustomStats:
    """
    All custom analyzers (such as calculating average working hours)
    must inherit this class and implement get_analysis.
    """

    def __init__(self, normalized_data: typing.Dict[str, list]):
        # TODO: We could further verify the structure of normalized_data
        self.normalized_data = normalized_data

    def get_analysis(self):
        raise NotImplemented


class WorkingHours(BaseCustomStats):

    def get_analysis(self):
        return self.get_working_hours()

    def get_working_hours(self) -> typing.OrderedDict[str, typing.Dict[str, float]]:
        ordered_results = OrderedDict()
        employee_working_hours_pair = {name: sum(time) for name, time in self.normalized_data.items()}
        max_working_employees = sorted(
            employee_working_hours_pair,
            key=employee_working_hours_pair.get,
            reverse=True
        )
        name: str
        for name in max_working_employees:
            ordered_results[name] = {'time': employee_working_hours_pair[name]}
        return ordered_results


class AverageWorkingMinutes(BaseCustomStats):

    def get_analysis(self):

        return self._get_average_working_minutes()

    def _get_average_working_minutes(self) -> typing.Dict[str, float]:
        result = {}
        total_number_of_registered_times: int = sum(
            len(employee_times) for employee_times in self.normalized_data.values()
        )
        total_working_minutes = sum([sum(employee_times) for employee_times in self.normalized_data.values()])
        averaging_working_mintutes = total_working_minutes / total_number_of_registered_times
        result['average_working_minutes'] = averaging_working_mintutes
        return result


class PickyStats:
    """
    This class puts everything together. To include more statistics, simply
    add the analyser class to the list of `analysers`.
    """
    parser = BasicParser
    analyzers = [AverageWorkingMinutes, ]
    formatter = DataFormatter

    def __init__(self, textfile: str):
        self.textfile = textfile
        self.normalized_data = self.parser(self.textfile).get_normalized_items()

    def get_all_stats(self, format='json'):
        ordered_working_hours = WorkingHours(self.normalized_data).get_working_hours()
        stats = self.get_stats()
        analysis_result = {}
        analysis_result['statistics'] = stats
        analysis_result['employees'] = ordered_working_hours

        final_result = DataFormatter(format=format, data=analysis_result).output()

        return final_result

    def get_stats(self):
        statistics = []
        for analyzer in self.analyzers:
            result = analyzer(self.normalized_data).get_analysis()
            statistics.append(result)
        return statistics


if __name__ == '__main__':
    with open('sample.rtf', 'r') as f:
        text = f.read()
        ins = PickyStats(textfile=text)
        r = ins.get_all_stats()
        print(r)
