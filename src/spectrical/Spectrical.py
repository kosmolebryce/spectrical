import re
import tkinter as tk
from tkinter import messagebox, scrolledtext


import re

class NMRAnalysisHelper:
    def __init__(self):
        self.common_shifts = {
            '1H NMR': {
                'TMS': 0,
                'Alkyl (R-CH3)': (0.7, 1.3),
                'Alkyl (R-CH2-R)': (1.2, 1.4),
                'Alkyl (R3CH)': (1.4, 1.7),
                'Allylic (R-CH2-C=C)': (1.6, 2.2),
                'Alkyne (RC≡C-H)': (2.0, 3.0),
                'Ketone (R-CO-CH3)': (2.1, 2.6),
                'Aldehyde (R-CHO)': (9.5, 10.1),
                'Alcohol (R-OH)': (0.5, 5.0),
                'Alcohol (R-CH2-OH)': (3.4, 4.0),
                'Ether (R-O-CH2-R)': (3.3, 3.9),
                'Ether (R-O-CH3)': (3.3, 3.8),
                'Ester (R-COO-CH3)': (3.6, 3.8),
                'Ester (R-COO-CH2-R)': (4.1, 4.3),
                'Alkene (R2C=CH2)': (4.6, 5.0),
                'Alkene (R2C=CH-R)': (5.2, 5.7),
                'Alkene (RHC=CH2)': (5.0, 5.5),
                'Aromatic (Ar-H)': (6.5, 8.5),
                'Benzyl (Ar-CH2-R)': (2.3, 2.8),
                'Phenol (Ar-OH)': (4.5, 7.7),
                'Carboxylic Acid (R-COOH)': (10.5, 12.0),
                'Amine (R-NH2)': (1.0, 3.0),
                'Amine (R2NH)': (1.2, 2.0),
                'Amide (R-CO-NH-R)': (5.0, 6.5),
                'Amide (R-CO-NH2)': (5.5, 7.5),
                'Thiol (R-SH)': (1.0, 1.5),
                'Phosphine (R3P-H)': (2.5, 4.5),
                'Silicon (R3Si-H)': (3.5, 5.0)
            },
            '13C NMR': {
                'Alkyl (R-CH3)': (0, 40),
                'Alkyl (R-CH2-R)': (15, 55),
                'Alkyl (R3CH)': (20, 60),
                'Allylic (R-CH2-C=C)': (20, 40),
                'Alkyne (RC≡C-H)': (60, 80),
                'Aromatic (Ar-C)': (100, 160),
                'Alkene (R2C=CR2)': (100, 150),
                'Ester (R-COO-R)': (160, 185),
                'Ketone (R-CO-R)': (190, 220),
                'Aldehyde (R-CHO)': (190, 200)
            },
            'Deuterated Solvent Residuals': {
                'Chloroform-d (CDCl3)': 7.26,
                'Dimethyl sulfoxide-d6 (DMSO-d6)': 2.50,
                'Acetone-d6': 2.05,
                'Methanol-d4': 3.31,
                'Water-d2 (D2O)': 4.79,
                'Benzene-d6': 7.16,
                'Acetonitrile-d3': 1.94
            }
        }

    def identify_functional_groups(self, shift, nmr_type='1H NMR'):
        identified = []
        for group, range_val in self.common_shifts[nmr_type].items():
            if isinstance(range_val, tuple):
                if range_val[0] <= shift <= range_val[1]:
                    identified.append(group)
            elif isinstance(range_val, (int, float)):
                if abs(shift - range_val) < 0.1:
                    identified.append(group)
        return identified

    def parse_input(self, input_string):
        input_string = re.sub(r'[\n,]', ' ', input_string)
        pattern = r'(\d+\.?\d*)'
        matches = re.findall(pattern, input_string)
        try:
            return [float(match) for match in matches]
        except ValueError:
            return []

    def analyze(self, input_string, nmr_type='1H NMR'):
        shifts = self.parse_input(input_string)
        if not shifts:
            return "No valid shifts found in input."
        analysis = []
        for shift in shifts:
            groups = self.identify_functional_groups(shift, nmr_type)
            if groups:
                analysis.append(f"{shift} ppm: Possible assignments - {', '.join(groups)}")
            else:
                analysis.append(f"{shift} ppm: No common assignments found")
        return '\n'.join(analysis)

class NMRAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NMR Analysis Helper")
        self.nmr_helper = NMRAnalysisHelper()

        self.label = tk.Label(root, text="Enter NMR Shifts (comma or line delimited, e.g., '0.9, 3.8' or '0.9\n3.8'):")
        self.label.pack(pady=10)

        self.input_text = tk.Text(root, height=5, width=60, wrap=tk.WORD)
        self.input_text.pack(pady=10)

        self.radio_var = tk.StringVar(value='1H NMR')
        self.radio_button_1h = tk.Radiobutton(root, text="1H NMR", variable=self.radio_var, value='1H NMR')
        self.radio_button_13c = tk.Radiobutton(root, text="13C NMR", variable=self.radio_var, value='13C NMR')
        self.radio_button_1h.pack()
        self.radio_button_13c.pack()

        self.analyze_button = tk.Button(root, text="Analyze", command=self.analyze_shifts)
        self.analyze_button.pack(pady=10)

        self.result_frame = tk.Frame(root)
        self.result_frame.pack(pady=10)

        self.result_text = scrolledtext.ScrolledText(self.result_frame, height=15, width=60, wrap=tk.WORD, state=tk.DISABLED)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def analyze_shifts(self):
        input_string = self.input_text.get("1.0", tk.END).strip()
        nmr_type = self.radio_var.get()
        result = self.nmr_helper.analyze(input_string, nmr_type)
        formatted_result = self.format_result(result)
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, formatted_result)
        self.result_text.config(state=tk.DISABLED)

    def format_result(self, result):
        lines = result.split('\n')
        formatted_lines = []
        for line in lines:
            if 'ppm' in line:
                shift, assignments = line.split(' ppm: ')
                formatted_lines.append(f"[{shift.strip()} ppm]")
                if 'No common assignments found' in assignments:
                    formatted_lines.append("No common assignments found\n")
                else:
                    groups = assignments.replace('Possible assignments - ', '').split(', ')
                    formatted_lines.append("Possible assignments:")
                    for group in groups:
                        formatted_lines.append(f"> {group}")
                    formatted_lines.append("")  # Add a blank line for separation
        return "\n".join(formatted_lines)

def main():
    root = tk.Tk()
    app = NMRAnalyzerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
