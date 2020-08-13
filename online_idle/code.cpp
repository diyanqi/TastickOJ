#include<bits/stdc++.h>
using namespace std;
int f[2005][2005];
int main(){
string s1,s2;
int i,j,k,la,lb;
cin>>s1>>s2>>k;
for(int i=0;i<2005;i++)
fill(f[i],f[i]+2005,0x7fffffff);
f[0][0]=0;
la=s1.size();
lb=s2.size();
for(i=1;i<=la;i++)
f[i][0]=f[i-1][0]+k;
for(i=1;i<=lb;i++)
f[0][i]=f[0][i-1]+k;
for(i=1;i<=la;i++){
for(j=1;j<=lb;j++){
f[i][j]=min(f[i][j],f[i-1][j-1]+abs(s1[i-1]-s2[j-1]));
f[i][j]=min(f[i][j],f[i-1][j]+k);
f[i][j]=min(f[i][j],f[i][j-1]+k);
}}
cout<<f[la][lb]<<endl;
return 0;
}