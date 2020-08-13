#include<iostream>
#include<cstring>
#include<cstdio>
#include<cstring>
using namespace std;
struct node 
{
    int data,rev,sum;
    node *son[2],*pre;
    bool judge();
    bool isroot();
    void pushdown();
    void update();
    void setson(node *child,int lr);
}lct[233];
int top,a,b;
node *getnew(int x)
{
    node *now=lct+ ++top;
    now->data=x;
    now->pre=now->son[1]=now->son[0]=lct;
    now->sum=0;
    now->rev=0;
    return now;
}
bool node::judge(){return pre->son[1]==this;}
bool node::isroot()
{
    if(pre==lct)return true;
    return !(pre->son[1]==this||pre->son[0]==this);
}
void node::pushdown()
{
    if(this==lct||!rev)return;
    swap(son[0],son[1]);
    son[0]->rev^=1;
    son[1]->rev^=1;
    rev=0;
}
void node::update(){sum=son[1]->sum+son[0]->sum+data;}
void node::setson(node *child,int lr)
{
    this->pushdown();
    child->pre=this;
    son[lr]=child;
    this->update();
}
void rotate(node *now)
{
    node *father=now->pre,*grandfa=father->pre;
    if(!father->isroot()) grandfa->pushdown();
    father->pushdown();now->pushdown();
    int lr=now->judge();
    father->setson(now->son[lr^1],lr);
    if(father->isroot()) now->pre=grandfa;
    else grandfa->setson(now,father->judge());
    now->setson(father,lr^1);
    father->update();now->update();
    if(grandfa!=lct) grandfa->update();
}
void splay(node *now)
{
    if(now->isroot())return;
    for(;!now->isroot();rotate(now))
    if(!now->pre->isroot())
    now->judge()==now->pre->judge()?rotate(now->pre):rotate(now);
}
node *access(node *now)
{
    node *last=lct;
    for(;now!=lct;last=now,now=now->pre)
    {
        splay(now);
        now->setson(last,1);
    }
    return last;
}
void changeroot(node *now)
{
    access(now)->rev^=1;
    splay(now);
}
void connect(node *x,node *y)
{
    changeroot(x);
    x->pre=y;
    access(x);
}
void cut(node *x,node *y)
{
    changeroot(x);
    access(y);
    splay(x);
    x->pushdown();
    x->son[1]=y->pre=lct;
    x->update();
}
int query(node *x,node *y)
{
    changeroot(x);
    node *now=access(y);
    return now->sum;
}
int main()
{
    scanf("%d%d",&a,&b);
    node *A=getnew(a);
    node *B=getnew(b);
    //连边 Link
        connect(A,B);
    //断边 Cut
        cut(A,B);
    //再连边orz Link again
        connect(A,B);
    printf("%d\n",query(A,B)); 
    return 0;
}