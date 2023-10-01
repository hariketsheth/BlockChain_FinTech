#include<bits/stdc++.h>
using namespace std;
#define ll long long int
#define pb push_back
 
ll find(ll *temp,ll l,ll r,ll x){
    while(l<r){
        ll m=(l+r)/2;
        if(temp[m]>=x)
          r=m;
        else
          l=m+1;  
    }
 
    return r;
}
 
vector<int> LIS (int n, vector<int> a) {
   // Write your code here
   vector<int> res;
 
   ll temp[n];
   res.push_back(1);
   temp[0]=a[0];
   ll i,j,x,len=1;
   
   for(i=1;i<n;i++){
         if(a[i]>=temp[len-1]){
             temp[len] = a[i];
             len++;
             res.push_back(len);
         }else{
             //x = find(temp,0,len-1,a[i]);
             x = upper_bound(temp,temp+len,a[i])-temp;
             temp[x] = a[i];
             res.push_back(x+1);
         }
   }
 
   return res;
}
 
int main() {
 
    ios::sync_with_stdio(0);
    cin.tie(0);
    int N;
    cin >> N;
    vector<int> Arr(N);
    for(int i_Arr = 0; i_Arr < N; i_Arr++)
    {
    	cin >> Arr[i_Arr];
    }
 
    vector<int> out_;
    out_ = LIS(N, Arr);
    cout << out_[0];
    for(int i_out_ = 1; i_out_ < out_.size(); i_out_++)
    {
    	cout << " " << out_[i_out_];
    }
}
