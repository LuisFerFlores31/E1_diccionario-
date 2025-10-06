#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

struct SubstrRank {
    int left_rank;
    int right_rank;
    int index;
    SubstrRank(int l, int r, int i) : left_rank(l), right_rank(r), index(i) {}
};

vector<int> make_ranks(const vector<SubstrRank>& substr_rank, int n) {
    vector<int> rank(n, -1);
    int r = 0;
    rank[substr_rank[0].index] = r;
    for (int i = 1; i < n; ++i) {
        if (substr_rank[i].left_rank != substr_rank[i-1].left_rank ||
            substr_rank[i].right_rank != substr_rank[i-1].right_rank) {
            r++;
        }
        rank[substr_rank[i].index] = r;
    }
    return rank;
}

vector<int> suffix_array(const string& T) {
    int n = T.size();
    vector<SubstrRank> substr_rank;
    for (int i = 0; i < n; ++i) {
        int left = T[i];
        int right = (i < n-1) ? T[i+1] : 0;
        substr_rank.emplace_back(left, right, i);
    }

    sort(substr_rank.begin(), substr_rank.end(), [](const SubstrRank& a, const SubstrRank& b) {
        return tie(a.left_rank, a.right_rank) < tie(b.left_rank, b.right_rank);
    });

    int l = 2;
    while (l < n) {
        vector<int> rank = make_ranks(substr_rank, n);
        for (int i = 0; i < n; ++i) {
            substr_rank[i].left_rank = rank[i];
            substr_rank[i].right_rank = (i + l < n) ? rank[i + l] : 0;
            substr_rank[i].index = i;
        }
        sort(substr_rank.begin(), substr_rank.end(), [](const SubstrRank& a, const SubstrRank& b) {
            return tie(a.left_rank, a.right_rank) < tie(b.left_rank, b.right_rank);
        });
        l *= 2;
    }

    vector<int> SA(n);
    for (int i = 0; i < n; ++i) {
        SA[i] = substr_rank[i].index;
    }
    return SA;
}

int main() {
    string text = "mississippi";
    vector<int> SA = suffix_array(text);
    for (int i : SA) {
        cout << i << " ";
    }
    cout << endl;
    return 0;
}