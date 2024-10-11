import openpyxl
import xml.etree.ElementTree as ET
import re

class ExcelParser:

    def __init__(self, file_path, namespace) -> None:
        self._file_path = file_path
        self._namespace = namespace
        self._root = None
        self.output_path = ""
        self._technology_dict = {}

    def file_path(self) -> str:
        return self._file_path
    
    def namespace(self) -> str:
        return self._namespace
    
    def output_path(self) -> str:
        return self.output_path

    def parse_excel(self, output_path):

        # Dictionary mapping LULC classes to workbook rows
        row_lulc_dict = {}
        
        # Open input Excel file
        with open(self._file_path, "rb") as f:

            # Open the workbook as read only
            workbook = openpyxl.load_workbook(f, True, False, True, False)

            # Check that all columns exist in the xCropProtection worksheet
            assert [x.value for x in workbook["xCropProtection"][1]] == ["PPP", "LULC type", "Application window",
                "Application rate [g/ha]", "In-crop buffer [m]", "In-field margin [m]", 
                "Spray-drift reduction [fraction]"], "The input table must have the following columns in order: PPP, LULC type, Application window, Application rate [g/ha], In-crop buffer [m], In-field margin [m], Spray-drift reduction [fraction]"

            # Set up the LULC and technology dictionaries
            for i, x in enumerate(workbook["xCropProtection"].iter_rows(max_col=7, min_row=2, values_only=False)):

                # Check that the required columns are present
                if not all(cell.value != None for cell in x[0:3]):
                    raise AssertionError(f"The 'PPP', 'LULC type', 'Application window', and 'Application rate [g/ha]' columns are required.")

                # Check the application window format
                if not re.match(r'\d\d?.\d\d?-\d\d?.\d\d?', str(x[2].value)):
                    raise AssertionError(f"All Application Windows must be in the format dd.mm-dd.mm")
                
                # If the spray drift cell is empty, the default value is 0
                spray_drift = 0 if x[6].value is None else x[6].value
                # First check that the spray-drift reduction is a float or int
                if not (type(spray_drift) == float or type(spray_drift) == int):
                    raise AssertionError(f"The spray-drift reduction value must be a decimal between 0 and 1, not " + str(spray_drift))
                # Then check that the drift reduction value is between the bounds
                if not (0 <= float(spray_drift) <= 1):
                    raise AssertionError(f"The spray-drift reduction value must be a decimal between 0 and 1, not " + str(spray_drift))

                # Add the lulc to a dictionary
                # keys: LULC values
                # values: a list of row indices whose target LULC is equal to the key
                lulc = x[1].value
                if lulc in row_lulc_dict:
                    row_lulc_dict[lulc].append(i)
                else:
                    row_lulc_dict[lulc] = [i]

                # Create the technology drift reduction dictionary
                # Keys: the spray drift reduction percent
                # values: the technology name
                if str(spray_drift) not in self._technology_dict:
                    self._technology_dict[str(spray_drift)] = str(spray_drift) + '-spray-drift-reduction'

            # Create the root xCropProtection element
            self._root = ET.Element('xCropProtection', attrib={'xmlns': self._namespace[''],
                                                                'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                                                                'xsi:schemaLocation': 'urn:xCropProtectionLandscapeScenarioParametrization ../model/core/components/xCropProtection/xCropProtection.xsd'})
            ppm_calendars = ET.SubElement(self._root, 'PPMCalendars')

            # Iterate through the LULC codes present in the input file
            for lulc in row_lulc_dict.keys():
                # Generate the PPMCalendar element for this LULC
                application_sequence = self.prepare_ppm_calendar(lulc, ppm_calendars)
                # Iterate through each row with the curent LULC type
                for row_id in row_lulc_dict[lulc]:
                    # Add 2 to row id because row indices start at 1 and need to skip the first row (headers)
                    self.write_application(application_sequence, workbook["xCropProtection"][row_id + 2])
        
        # Create the technology xml elements based on the spray-drift reduction values in the input file
        self.generate_technologies(self._root)
        tree = ET.ElementTree(self._root)
        ET.indent(tree)
        tree.write(output_path, encoding='utf-8', xml_declaration=True)

    # Generates individual PPM Calendars for a given LULC. Returns the ApplicationSequence element (child)
    def prepare_ppm_calendar(self, lulc: int, ppm_calendars: ET.SubElement) -> ET.SubElement:

        calendar = ET.SubElement(ppm_calendars, 'PPMCalendar')
        # Set TemporalValidity and TargetCrops 
        ET.SubElement(calendar, 'TemporalValidity', attrib={'scales': 'time/simulation'}).text = 'always'
        ET.SubElement(calendar, 'TargetCrops', attrib={'type': 'list[int]', 'scales': 'global'}).text = str(lulc)
        
        indications = ET.SubElement(calendar, 'Indications')
        indication = ET.SubElement(indications, 'Indication', attrib={'type': 'xCropProtection.ChoiceDistribution', 'scales': 'time/year, space/base_geometry'})
        application_seq = ET.SubElement(indication, 'ApplicationSequence', attrib={'probability': '1.0'})
        
        return application_seq

    # Generates an individual application for a given row in the input Excel file
    def write_application(self, application_sequence, row):

        # Store application info
        application_info = [x.value for x in row]

        # Application
        application = ET.SubElement(application_sequence, 'Application')
        # Tank
        tank = ET.SubElement(application, 'Tank')
        # Product name
        ET.SubElement(tank, 'Products', attrib={'type': 'list[str]', 'scales': 'other/products'}).text = str(application_info[0])
        # Application rates
        app_rates = ET.SubElement(tank, 'ApplicationRates', attrib={'scales': 'other/products'})
        # Application rate of the product
        ET.SubElement(app_rates, 'ApplicationRate', attrib={'type': 'float', 'unit': 'g/ha', 'scales': 'global'}).text = str(application_info[3])
        # Application window
        ET.SubElement(application, 'ApplicationWindow', attrib={'type': 'xCropProtection.MonthDaySpan', 'scales': 'global'}).text = self.convert_date(application_info[2])
        # Technology
        technology = '0' if str(application_info[6]) == 'None' else str(application_info[6])
        ET.SubElement(application, 'Technology', attrib={'scales': 'global'}).text = self._technology_dict[technology]
        # In-crop buffer
        in_crop_buffer = '0' if str(application_info[4]) == 'None' else str(application_info[4])
        ET.SubElement(application, 'InCropBuffer', attrib={'type': 'float', 'unit': 'm', 'scales': 'global'}).text = in_crop_buffer
        # In-field margin
        in_field_margin = '0' if str(application_info[5]) == 'None' else str(application_info[5])
        ET.SubElement(application, 'InFieldMargin', attrib={'type': 'float', 'unit': 'm', 'scales': 'global'}).text = in_field_margin

    # Convert from European to US date format
    def convert_date(self, window: str) -> str:

        date_range = window.split('-')
        # Swap from day-month to month-day. Pad with a leading 0 if necessary
        start_date = date_range[0].split('.')[1].rjust(2, '0') + '-' + date_range[0].split('.')[0].rjust(2, '0')
        end_date = date_range[1].split('.')[1].rjust(2, '0') + '-' + date_range[1].split('.')[0].rjust(2, '0')
        return start_date + ' to ' + end_date

    # Generate Technology elements based on the technology dictionary
    def generate_technologies(self, xcp_root):

        tech_root = ET.SubElement(xcp_root, 'Technologies')

        # Create a technology element for each unique spray drift reduction value
        for reduction, name in self._technology_dict.items():
            technology = ET.SubElement(tech_root, 'Technology')
            ET.SubElement(technology, 'TechnologyName', attrib={'scales': 'global'}).text = str(name)
            ET.SubElement(technology, 'DriftReduction', attrib={'type': 'float', 'unit': '1', 'scales': 'global'}).text = str(reduction)
        