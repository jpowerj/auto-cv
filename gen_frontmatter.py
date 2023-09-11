import glob
from io import StringIO
import os

import yaml

latex_start = """% content.tex
% ---
"""
latex_end = """
% ---"""

def convert_to_frontmatter(fpath):
    with open(fpath, 'r', encoding='utf-8') as infile:
        data_dict = yaml.safe_load(infile)
    fname = os.path.basename(fpath)
    data_name = fname.split(".")[0]
    # We're going to have the whole thing indented under the filename as key
    #print(data_dict)
    my_io = StringIO()
    yaml.safe_dump(data_dict, stream=my_io, sort_keys=True)
    yaml_str = my_io.getvalue()
    yaml_lines = yaml_str.split("\n")
    # Add latex comments
    latex_lines = ["%   " + yaml_line for yaml_line in yaml_lines if yaml_line != ""]
    latex_lines = ["% " + data_name + ":"] + latex_lines
    # And add the start and end lines
    #latex_lines = ["% ---"] + latex_lines + ["% ---"]
    latex_content = "\n".join(latex_lines)
    return latex_content

def main():
    # Load the yaml from _data
    yaml_path = os.path.join(".","_data")
    yaml_fpaths = glob.glob(os.path.join(yaml_path, "*.yml"))
    # But skip the webpage-specific ones
    exclude_data = ["navigation","links","tutoring"]
    fm_strs = []
    for cur_fpath in yaml_fpaths:
        cur_fname = os.path.basename(cur_fpath)
        cur_data_name = cur_fname.split(".")[0]
        if cur_data_name in exclude_data:
            continue
        cur_fm_str = convert_to_frontmatter(cur_fpath)
        fm_strs.append(cur_fm_str)
    fm_str = "\n".join(fm_strs)
    # Add the explicit start and end
    fm_str = "% ---\n" + fm_str + "\n% ---"
    # And save
    output_fname = "content.tex"
    with open(output_fname, 'w', encoding='utf-8') as outfile:
        outfile.write(fm_str)
    print(f"Saved to {output_fname}")

if __name__ == "__main__":
    main()