import os 

def read_log(file):
    try:
        with open(file=file, mode='r') as f:
            lines = f.read()
        return lines
    except FileNotFoundError:
        return "File not found"
    except PermissionError:
        return "don't have permission to access file"
    except Exception as e:
        print(f"Something else broke: {e}")

def parse_line():
    pass

def total_lines():
    pass

def count_per_level():
    pass

def common_messages():
    pass

def save_report_to_json():
    pass

if __name__ == "__main__":
    print(os.getcwd())
    lines = read_log("../sample.log")
  
  