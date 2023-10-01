# coding=utf-8
import cPickle as pickle
import time
import traceback

from joblib import Parallel, delayed

from cal_wfp_features import WFPFeatures
from environments import PREFIX, NEG_WEBSITE_NUM


def producer(page_seq_dict):
    for page in page_seq_dict:
        for page_index in page_seq_dict[page]:  # page_seq_dict[page] is a list of page_index with size 90(aka. 90 instances)
            yield page, page_index  # page_index is a {flow:[trace aka [[ts, len]] ]}


def neg_producer(neg_raw_data):
    for flow in neg_raw_data:
        yield 'unmonitored', {flow: neg_raw_data[flow][0]}


def seq2features(data, is_neg_data):
    # data  {page:[90 instances{flow:[trace]}]}
    if is_neg_data:
        page_dict = Parallel(n_jobs=-1)(
            delayed(extract_features)(page, page_index) for page, page_index in neg_producer(data))
    else:
        # page_dict is tuple(page,page_index_features{flow,features array[]})
        # page_index_features[flow] is a list of features which means each flow has more than 1 features array
        page_dict = Parallel(n_jobs=-1)(
            delayed(extract_features)(page, page_index) for page, page_index in producer(data))
    page_features_dict = dict()

    for page, page_index_features in page_dict:
        if page not in page_features_dict:
            page_features_dict[page] = []
        page_features_dict[page].append(page_index_features)
    # page_features_dict is {page:[{flow:features array[]}]}
    return page_features_dict


def extract_features(page, page_index):
    """
     format is {label:[[ts, len],[ts, len]], [[], [],...],...}
    """
    count = 0
    page_index_features = dict()
    for flow in page_index:  # page_index is a {flow:[trace]}
        if flow not in page_index_features:
            page_index_features[flow] = []
        for ii, url in enumerate(page_index[flow]):  # url is [[ts, len],[ts, len]], ii is the index of the url
            print 'Extracting features in %s %s %d' % (page, flow, ii)
            try:
                #  page_index_features[flow] is a list of features which means each flow has more than 1 features array
                page_index_features[flow].append(compute_features(url))
            except Exception as e:
                print traceback.print_exc()
                print 'error in extract features of %d  ' % count, e
            finally:
                count += 1
    return page, page_index_features


# @timeout_decorator.timeout(60)
def compute_features(seq):
    return WFPFeatures(seq).get_all_features()


if __name__ == '__main__':
    """
     format is {label:[[ts, len],[ts, len],...], [[], [],...],...}
    """
    #data_raw.pickle
    # data_raw = pickle.load(open(PREFIX+'data/data_raw1.pickle', 'rb'))
    # all_ret = seq2features(data_raw, False)
    # pickle.dump(all_ret, open(PREFIX+'data/data_feats1.pickle', 'wb'), protocol=2)

    # data_raw = pickle.load(open(PREFIX + 'data_raw.pickle', 'rb'))
    # all_ret = seq2features(data_raw, False)
    # pickle.dump(all_ret, open(PREFIX + 'data_feats.pickle', 'wb'), protocol=2)
    neg_data_raw = pickle.load(open(PREFIX + 'neg_data_raw.pickle', 'rb'))
    # generate features of neg_data

    # {page:[90 instances{flow:trace}]}
    # neg_data_raw = pickle.load(open(PREFIX+'data/neg_data_raw.pickle', 'rb'))
    keys = neg_data_raw.keys()
    # 选多少负例

    keys = keys[0:NEG_WEBSITE_NUM]
    neg_data_raw = {key: value for key, value in neg_data_raw.items() if key in keys}
    start = time.time()
    all_ret = seq2features(neg_data_raw, True)
    end = time.time()
    print 'Extraction done,time taken:%d s,Ready to dump' % (end - start)

    start = time.time()
    # 选取三千个网站
    pickle.dump(all_ret, open('common-data/neg_data_feats_3000.pickle', 'wb'), protocol=2)
    end = time.time()
    print 'Dump done,time taken:%d s' % (end - start)
    print 'Dump done'
