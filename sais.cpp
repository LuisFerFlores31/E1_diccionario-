#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <algorithm>
#include <string>

using namespace std;

map<int, pair<int, int>> getBuckets(const vector<int>& T) {
    map<int, int> count;
    map<int, pair<int, int>> buckets;
    for (int c : T) count[c]++;
    int start = 0;
    for (auto& kv : count) {
        buckets[kv.first] = {start, start + kv.second};
        start += kv.second;
    }
    return buckets;
}

vector<int> sais(const vector<int>& T) {
    int n = T.size();
    vector<char> t(n, '_');
    t[n - 1] = 'S';
    for (int i = n - 1; i > 0; --i) {
        if (T[i - 1] == T[i]) t[i - 1] = t[i];
        else t[i - 1] = (T[i - 1] < T[i]) ? 'S' : 'L';
    }

    auto buckets = getBuckets(T);
    map<int, int> count;
    vector<int> SA(n, -1);
    map<int, int> LMS;
    int end = -1;
    for (int i = n - 1; i > 0; --i) {
        if (t[i] == 'S' && t[i - 1] == 'L') {
            int revoffset = ++count[T[i]];
            SA[buckets[T[i]].second - revoffset] = i;
            if (end != -1) LMS[i] = end;
            end = i;
        }
    }
    LMS[n - 1] = n - 1;

    count.clear();
    for (int i = 0; i < n; ++i) {
        if (SA[i] >= 0 && SA[i] > 0 && t[SA[i] - 1] == 'L') {
            int symbol = T[SA[i] - 1];
            int offset = count[symbol]++;
            SA[buckets[symbol].first + offset] = SA[i] - 1;
        }
    }

    count.clear();
    for (int i = n - 1; i > 0; --i) {
        if (SA[i] > 0 && t[SA[i] - 1] == 'S') {
            int symbol = T[SA[i] - 1];
            int revoffset = ++count[symbol];
            SA[buckets[symbol].second - revoffset] = SA[i] - 1;
        }
    }

    vector<int> namesp(n, -1);
    int name = 0;
    int prev = -1;
    for (int i = 0; i < n; ++i) {
        if (SA[i] >= 0 && SA[i] > 0 && t[SA[i]] == 'S' && t[SA[i] - 1] == 'L') {
            if (prev != -1) {
                int a_start = SA[prev], a_end = LMS.count(SA[prev]) ? LMS[SA[prev]] : n;
                int b_start = SA[i], b_end = LMS.count(SA[i]) ? LMS[SA[i]] : n;
                vector<int> a(T.begin() + a_start, T.begin() + a_end);
                vector<int> b(T.begin() + b_start, T.begin() + b_end);
                if (a != b) name++;
            }
            prev = i;
            namesp[SA[i]] = name;
        }
    }

    vector<int> names, SApIdx;
    for (int i = 0; i < n; ++i) {
        if (namesp[i] != -1) {
            names.push_back(namesp[i]);
            SApIdx.push_back(i);
        }
    }

    if (name < (int)names.size() - 1) {
        names = sais(names);
    }

    reverse(names.begin(), names.end());

    SA.assign(n, -1);
    count.clear();
    for (int i = 0; i < (int)names.size(); ++i) {
        int pos = SApIdx[names[i]];
        int revoffset = ++count[T[pos]];
        SA[buckets[T[pos]].second - revoffset] = pos;
    }

    count.clear();
    for (int i = 0; i < n; ++i) {
        if (SA[i] >= 0 && SA[i] > 0 && t[SA[i] - 1] == 'L') {
            int symbol = T[SA[i] - 1];
            int offset = count[symbol]++;
            SA[buckets[symbol].first + offset] = SA[i] - 1;
        }
    }

    count.clear();
    for (int i = n - 1; i > 0; --i) {
        if (SA[i] > 0 && t[SA[i] - 1] == 'S') {
            int symbol = T[SA[i] - 1];
            int revoffset = ++count[symbol];
            SA[buckets[symbol].second - revoffset] = SA[i] - 1;
        }
    }

    return SA;
}

vector<int> string_to_intvec(const string& s) {
    vector<int> T;
    for (char c : s) T.push_back((int)c);
    return T;
}

int main(int argc, char* argv[]) {
    string text;
    if (argc < 2) {
        text = "GTCCCGATGTCATGTCAGGA$";
    } else {
        ifstream file(argv[1], ios::in | ios::binary);
        if (!file) {
            cerr << "Error: Cannot open file " << argv[1] << endl;
            return 1;
        }
        text.assign((istreambuf_iterator<char>(file)), istreambuf_iterator<char>());
        text += "$";
    }
    vector<int> T = string_to_intvec(text);
    vector<int> SA = sais(T);
    cout << "Suffix array size: " << SA.size() << endl;
    // Uncomment to print the suffix array
    // for (int i : SA) cout << i << " ";
    // cout << endl;
    return 0;
}