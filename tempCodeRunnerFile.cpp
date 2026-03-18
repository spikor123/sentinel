#include <iostream>
using namespace std;

// Function prototype
void sort(int arr[], int size);

int main(){
    int arr[]={2,4,2,45,6};
    int size=sizeof(arr)/sizeof(arr[0]);
    for(int element:arr){
        cout<<element<<" ";

    }
    sort(arr,size);
    for(int element:arr){
     cout<<element<<" ";   
    }
    
    return 0;
}

void sort(int arr[],int size){
    int temp=0;
    for(int i=0;i<size-1;i++){
        for(int j=0;j<size-i-1;j++){
            if(arr[j]>arr[j+1]){
                temp=arr[j];
                arr[j]=arr[j+1];
                arr[j+1]=temp;
            }
        }

    }
}