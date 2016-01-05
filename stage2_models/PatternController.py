"""
    Class PatternController:
        it judge the host-model whether to model study or anomaly detection.
"""
__author__ = 'j-lijiawei'


class PatternController:
    def __init__(self, url_amount=190000, durl_amount=700, sip_amount=900):
        # minimum threshold of the urls amount in a host model
        self.url_amount = url_amount
        # minimum threshold of the different url types in a host model
        self.dif_url_amount = durl_amount
        # minimum threshold of the different sips in a host model
        self.sip_amount = sip_amount

    def judgePattern(self, a_host_model):
        """
        :param a_host_model: HostModel -- the host model that be judged
        :return: 'Anomaly' (the module can be used to detect) or 'Module study' (the module still need to study)
        """
        host_urls_amount = a_host_model.getUrlAmount()
        host_dif_urls_amount = a_host_model.getDifUrlAmount()
        host_sip_amount = a_host_model.getSipAmount()
        if host_urls_amount >= self.url_amount and host_dif_urls_amount >= self.dif_url_amount and host_sip_amount >= self.sip_amount:
            return 'Anomaly detection'
        else:
            return 'Module study'
