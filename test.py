import pickle

if __name__ == '__main__':
    s1 = 'neg_data_raw.pickle'
    s2 = 'data_raw.pickle'
    s8 = 'data_raw1.pickle'
    s3 = 'ray_page_dict_flow_feats_del.pickle'
    s4 = 'data_feats.pickle'
    s5 = 'neg_data_feats.pickle'
    s6 = 'neg_data_raw_for_bg.pickle'
    s7 = 'test2/data/data_raw1.pickle'
    l = 'cn.bing.com_lcs_kv_list.pickle'
    # lcs = pickle.load(open('data/lcs/' + l, 'rb'))
    f2 = pickle.load(open('data/' + s2, 'rb'))
    f1 = pickle.load(open('data/' + s1, 'rb'))

    f3 = pickle.load(open('data/' + s6, 'rb'))
    f4 = pickle.load(open('data/' + s8,'rb'))
    # neg_data_raw_for_bg = dict()
    # for x in f.keys():
    #     neg_data_raw_for_bg[x] = f[x][0]
    # pickle.dump(neg_data_raw_for_bg, open('data/neg_data_raw_for_bg.pickle', 'wb'), protocol=2)
    print "ok"
