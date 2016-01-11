"""
    Class AnomalyWriter:
        Writing the anomaly detection result.
"""

__author__ = 'j-lijiawei'


class ResultWriter:
    def __init__(self, outfile_address):
        """
        :param outfile_address: str
        """
        self.__outfile_address = outfile_address
        # clear the file
        with open(self.__outfile_address, 'wb') as outfile:
            outfile.truncate()

        self.outfile_address_2 = 'E:\\Program Files\\PyCharm\\myWorkSpace\\WUA\\data_container\\Time_analysis\\HuaJiao_wvs_1113_result'
        with open(self.outfile_address_2, 'wb') as outfile:
            outfile.truncate()

    def writeResult(self, a_record, a_anomaly_status):
        """
        :param a_record: UrlRecord
        :param a_anomaly_status: dict --> {'Result': boolean, 'Reason': str}
        """
        try:
            with open(self.__outfile_address, 'ab') as outfile:
                outfile.write('%s\n' % a_anomaly_status['Reason'])
                outfile.write('\t%s\n' % a_record.get_url())
        except IOError:
            print 'AnomalyWriter IO ERROR'
            raise

    def writeCompleteResult(self, a_record, a_anomaly_status):
        """
        :param a_record: UrlRecord
        :param a_anomaly_status: dict --> {'Result': boolean, 'Reason': str}
        """
        try:
            with open(self.__outfile_address, 'ab') as outfile:
                outfile.write('%s\n' % a_anomaly_status['Reason'])
                outfile.write('\t%s\n' % a_record.get_content())
        except IOError:
            print 'AnomalyWriter IO ERROR'
            raise

    def writeTimeAttribute(self, a_record):
        with open(self.outfile_address_2, 'ab') as outfile:
            outfile.write('%s\t%s\n' % (a_record.get_timestamp(), a_record.get_url()))

    def writePathResult(self, a_record, a_anomaly_status):
        """
        :param a_record: UrlRecord
        :param a_anomaly_status: dict --> {'Result': boolean, 'path_para': float}
        """
        try:
            with open(self.__outfile_address, 'ab') as outfile:
                outfile.write('%s\n' % a_record.get_url())
                outfile.write('\t%s\n' % a_anomaly_status['path_para'])
        except IOError:
            print 'AnomalyWriter IO ERROR'
            raise
