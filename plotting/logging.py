class Logger:
    @staticmethod
    def write(category, *values):
        with open("logfiles/" + category + ".log", "a") as f:
            for v in values:
                f.write(str(v))
                f.write(",")
            f.write("\n")
