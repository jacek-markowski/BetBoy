# -*- coding: utf-8 -*-
"""
Copyright 2013 Jacek Markowski

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys
import os
import platform
system = platform.system()
if system == 'Windows':
    new_line = '\r\n'
    from pyfann_win import libfann
elif system == 'Linux':
    new_line = '\n'
    from pyfann import libfann
elif system == 'Darwin':
    new_line = '\r'
else:
    new_line = '\r\n'

print sys.argv[:]
def start(file_in=sys.argv[1],
          connection_rate =float(sys.argv[2]),
          num_neurons_hidden = int(sys.argv[3]),
          desired_error =float(sys.argv[4]),
          max_iterations = int(sys.argv[5]),
          iterations_between_reports = int(sys.argv[6]),
          function_output = 'libfann.'+sys.argv[7],
          function_hidden = 'libfann.'+sys.argv[8],
          training_algorithm = 'libfann.'+sys.argv[9],
          file_out= sys.argv[10]):
    ''' Learning network'''
    title = open(os.path.join('export', '')+file_in, 'r').readline()
    sets, num_input, num_output = title.split(' ')
    num_input = int(num_input)
    num_output = int(num_output)
    print num_input, num_output
    # create training data, and ann object
    train_data = libfann.training_data()
    train_data.read_train_from_file(os.path.join('export', '')+file_in)
    ann = libfann.neural_net()
    ann.create_sparse_array(connection_rate, (num_input, num_neurons_hidden,
                                              num_output))
    ## start training the network
    ann.set_activation_function_output(eval(function_output))
    ann.set_activation_function_hidden(eval(function_hidden))
    ann.set_bit_fail_limit(0.1)
    ann.set_rprop_increase_factor(1.225)
    ann.set_rprop_decrease_factor(0.325)
    ann.set_rprop_delta_min(-10.0)
    ann.set_rprop_delta_max(10.0)
    ann.set_training_algorithm(eval(training_algorithm))
    ann.set_train_stop_function(libfann.STOPFUNC_MSE)
    ann.train_on_data(train_data, max_iterations,
                      iterations_between_reports, desired_error)
    # save network to disk
    ann.save(os.path.join('net','')+file_out)
   
if __name__ == "__main__":
    start()
