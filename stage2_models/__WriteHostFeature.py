__author__ = 'j-lijiawei'


def write(test_host_feature, host_feature_stores_address):
    with open(host_feature_stores_address, 'wb') as clear_file:
        clear_file.truncate()

    with open(host_feature_stores_address, 'ab') as outfile:
        t_single_element_count, t_double_element_count = test_host_feature['path_element_count']
        outfile.write('Single Element Count:\n')
        for t_element, t_count in t_single_element_count.items():
            outfile.write('\t%s\t%d\n' % (repr(t_element), t_count))
        outfile.write('\n\nDouble Element Count:\n')
        for t_element, t_count in t_double_element_count.items():
            outfile.write('\t%s\t%d\n' % (repr(t_element), t_count))

        value_special_symbol_prop = test_host_feature['value_specialSymbol_prop']
        outfile.write('\n\nValue Special Symbol Probability:\n')
        for t_path, t_variable_dict in value_special_symbol_prop.items():
            outfile.write('\t%s\n' % t_path)
            for t_variable, t_specialSymbol_dict in t_variable_dict.items():
                outfile.write('\t\t%s\n' % t_variable)
                for specialSymbol, t_prop in t_specialSymbol_dict.items():
                    outfile.write('\t\t\t%s:\t%f\n' % (specialSymbol, t_prop))

        variable_enumeration = test_host_feature['variable_enumeration']
        outfile.write('\n\nVariable Enumeration:\n')
        for t_path, t_variable_dict in variable_enumeration.items():
            outfile.write('\t%s\n' % t_path)
            for t_variable, t_enumerated_type in t_variable_dict.items():
                outfile.write('\t\t%s\t%s\n' % (t_variable, t_enumerated_type))

        t_variable_composition_pool = test_host_feature['variable_composition_pool']
        outfile.write('\n\nVariable Composition:\n')
        for t_path, t_variable_composition_set in t_variable_composition_pool.items():
            outfile.write('\t%s:\n' % t_path)
            for a_t_variable_composition in t_variable_composition_set:
                outfile.write('\t\t%s:\n' % a_t_variable_composition)

        t_variable_order_rule = test_host_feature['variable_order_rule']
        outfile.write('\n\nVariable Order Rule:\n')
        for t_path, t_variable_order_set in t_variable_order_rule.items():
            outfile.write('\t%s:\n' % t_path)
            for t_variable_order in t_variable_order_set:
                outfile.write('\t\t%s:\n' % repr(t_variable_order))

        t_value_length_distribution = test_host_feature['value_length_distribution']
        outfile.write('\n\nValue Length Distribution:\n')
        for t_path, t_variable_dict in t_value_length_distribution.items():
            outfile.write('\t%s:\n' % t_path)
            for t_variable, t_distribution in t_variable_dict.items():
                outfile.write('\t\t%s:\n' % t_variable)
                outfile.write('\t\t\tmean: %f\n' % t_distribution['mean'])
                outfile.write('\t\t\tvariance: %f\n' % t_distribution['variance'])

        t_value_distribution1 = test_host_feature['value_distribution1']
        outfile.write('\n\nValue Distribution1:\n')
        for t_path, t_variable_dict in t_value_distribution1.items():
            outfile.write('\t%s:\n' % t_path)
            for t_variable, t_distribution in t_variable_dict.items():
                outfile.write('\t\t%s:\n' % t_variable)
                for t_i, t_prop in enumerate(t_distribution):
                    outfile.write('\t\t\tP%d: %f\n' % (t_i, t_prop))

        t_value_distribution2 = test_host_feature['value_distribution2']
        outfile.write('\n\nValue Distribution2:\n')
        for t_path, t_variable_dict in t_value_distribution2.items():
            outfile.write('\t%s:\n' % t_path)
            for t_variable, t_distribution in t_variable_dict.items():
                outfile.write('\t\t%s:\n' % t_variable)
                for t_i, t_prop in enumerate(t_distribution):
                    outfile.write('\t\t\tP%d: %f\n' % (t_i, t_prop))
