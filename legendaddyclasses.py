import csv
import legendaddyfunctions as ldf


class Summary():
    """Represents a Summary."""

    def __init__(self, name):
        """Initialize Summary object."""
        self.name = name
        self.title = None
        """
        An array of services, services will be Dictionaries, for example: 
        [
            {'job_description': 'CARD PROCESSING FEE', 'num_customers': '1', 'amount': '$71.10', 'avg_per_customer': '$71.10'}, 
            {'job_description': 'COMMERCIAL EXTERIOR WINDOW WASH', 'num_customers': '28', 'amount': '$13,572.78', 'avg_per_customer': '$484.74'}
        ]
        """
        self.services = []


class Details():
    """Represents Details section for each service"""

    def __init__(self, name):
        """Initialize a Details object."""
        self.name = name
        """
        A Dictionary of services -> service details (individual records of )
        {
            'CARD PROCESSING FEE': [
                {'invoice': '3316', 'customer': 'Wiser 2*, Nicole', 'job_date': 'Mar 10, 2022', 'amount': '$71.10', 'assigned_to': 'SHANE B.,David Peters'}
            ], 
            'COMMERCIAL PRESSURE WASH': [
                {'invoice': '3254', 'customer': 'The Habit Burger Grill*', 'job_date': 'Feb 9, 2022', 'amount': '$250.00', 'assigned_to': 'RICHLAND CREW,Colby V.,Joshuwa Steele,David Peters'}, 
                {'invoice': '3350', 'customer': 'The Habit Burger Grill*', 'job_date': 'Mar 16, 2022', 'amount': '$250.00', 'assigned_to': 'KENNEWICK CREW,Joshuwa Steele'}
            ],
            'DECK GLASS': [{...}]
        }
        """
        self.details = {}


class Job():
    """Represents a job to read in summary, details for two time periods and produce outputs"""

    def __init__(self, name, filename):
        """Initialize a Job object."""
        self.name = name
        self.filename = filename
        self.summary = None
        self.details = None

    def read(self):

        with open(self.filename, newline='') as csvfile:

            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            line_num = 0
            in_summary = False
            self.summary = Summary('Summary')
            in_detail = False
            self.details = Details('Details')

            for line in csvreader:
                line_num += 1

                if ldf.is_blank_line(line):
                    continue

                """Consume title"""
                if line_num == 1:
                    self.summary.title = line[0]
                    continue

                if line[0] == 'Summary':
                    in_summary = True
                    continue

                if line[0] == 'Details':
                    in_summary = False
                    in_detail = True
                    continue

                if in_summary:
                    """
                    "Jobs/Description of Service","# of Customers","Amount","Avg per Customer"
                    """
                    if line[0].startswith("Jobs"):
                        """Skip header line"""
                        continue

                    self.summary.services.append({
                        'job_description': line[0],
                        'num_customers': line[1],
                        'amount': line[2],
                        'avg_per_customer': line[3]
                    })
                    continue

                if in_detail:
                    """
                    "CARD PROCESSING FEE"
                    "Invoice","Customer","Job Date","Amount","Assigned To"
                    "3316","Wiser 2*, Nicole","Mar 10, 2022","$71.10","SHANE B.,David Peters"
                    "Total Sales for CARD PROCESSING FEE"," "," ","$71.10" 
                    """
                    if (len(line) == 1):
                        service = line[0]
                        self.details.details[line[0]] = []
                        continue

                    """
                    "Invoice","Customer","Job Date","Amount","Assigned To"
                    """
                    if (line[0].startswith("Invoice")):
                        """Skip header line"""
                        continue

                    if (line[0].startswith("Total")):
                        self.details.total_sales = line[3]
                        service = ''
                        continue

                    new_detail = {
                        'invoice': line[0],
                        'customer': line[1],
                        'job_date': line[2],
                        'amount': line[3],
                        'assigned_to': line[4]
                    }

                    service_record = self.details.details[service]
                    service_record.append(new_detail)
                    continue
