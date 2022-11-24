from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))

        s = self.read_input()
        step_n = len(s) / len(self.workers)
        step_left = len(s) % len(self.workers)

        # map
        mapped = []
        current_l = 0
        current_r = -1
        for i in xrange(0, len(self.workers)):
            print("map %d" % i)

            if i < step_left:
                current_r += step_n + 1
            else:
                current_r += step_n

            mapped.append(self.workers[i].mymap(s,  str(current_l), str(current_r)))
            
            current_l = current_r + 1

        pal_number = self.myreduce(mapped)
        self.write_output(pal_number)
        print("Job Finished")

    @staticmethod
    @expose
    def mymap(full_s, l, r):
        print('full_s = ', full_s)
        print('l = ', l)
        print('r = ', r)
        l = int(l)
        r = int(r)
        pal_number = 0

        for i in xrange(l, r+1):
            pal_number += Solver.find_palindromes(full_s, i)

        return pal_number

    @staticmethod
    @expose
    def myreduce(mapped):
        print("reduce")
        output = 0

        for pal_number in mapped:
            print("reduce loop")
            output += pal_number.value
        print("reduce done")
        return output

    def read_input(self):
        f = open(self.input_file_name, 'r')
        s = f.readline()
        f.close()
        return s

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str(output))
        f.write('\n')
        f.close()
        print("output done")

    @staticmethod
    @expose
    def find_palindromes(s, pos):
        cnt = 0
        length = len(s)

        l = pos
        r = pos
        # Odd length palindromes
        while l >= 0 and r < length:
            if s[l] == s[r]:
                cnt += 1
            else:
                break
            l -= 1
            r += 1
        
        # Even length palindromes
        l = pos
        r = pos+1
        while l >= 0 and r < length:
            if s[l] == s[r]:
                cnt += 1
            else:
                break
            l -= 1
            r += 1
        return cnt
