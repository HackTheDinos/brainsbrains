#include <stdio.h>
#include "buildTwoLayerTriangles.c"

void printTriangle(int tri[][3]);

int main() {
    
    // generate example data to work with. just 2 layers with a differently sloped line
    int n1 = 3;
    int n2 = 12;

    int l1[n1][2];
    int l2[n2][2];

    int i = 0;

    for(i=0; i<n1; i++) {
        l1[i][0] = i;
        l1[i][1] = i*2;
    }

    for(i=0; i<n2; i++) {
        l2[i][0] = i;
        l2[i][1] = i/2;
    }
    
    // do triangle generation
    int triangles[n1+n2][3][3];
    
    generateTriangles(triangles, l1, n1, 100, l2, n2, 101);

    // print results
    for(i=0; i<n1+n2; i++) {
        printTriangle(triangles[i]);
    }

    return 0;
}

void printTriangle(int tri[][3]) {
    int i,j;
    for(i=0; i<3; i++) {
        printf("[");
        for(j=0; j<3; j++) {
            printf("%d,", tri[i][j]);
        }
        printf("] ");
    }
    printf("\n");
}

