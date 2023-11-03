#include <stdio.h>
#include <winsock2.h>                       // Windows Socket
#include <iostream>

void sWrite(char *SCPI){
    printf("sWrite: %s\n", SCPI);
}

int sQuery(char *SCPI){
    sWrite(SCPI);
    printf("sQuery: %s\n", SCPI);
    return 0;
}

int main(){
 
    for(int i = 0; i < 5; i++ ) {
        printf("Hello World %d\n", i);
    }
    sQuery("asdf");
}
