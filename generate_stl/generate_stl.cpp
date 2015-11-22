#include <stdio.h>

void TwoLayerTriangles(int l1[][2], int n1, int l2[][2], int n2);

int main() {
    
    // generate example data to work with. just 2 layers with a differently sloped line
    int n1 = 10;
    int n2 = 40;

    int l1[n1][2];
    int l2[n2][2];

    for(int i=0; i<n1; i++) {
        l1[i][0] = i;
        l1[i][1] = i*2;
    }

    for(int i=0; i<n2; i++) {
        l2[i][0] = i;
        l2[i][1] = i/2;
    }
        
    TwoLayerTriangles(l1, n1, l2, n2);

    return 0;
}

void TwoLayerTriangles(int l1[][2], int n1, int l2[][2], int n2) {
    
    // just print the array values
    for(int i=0; i<n1; i++) {
        for(int j=0; j<2; j++) {
            printf("%d ", l1[i][j]);
        }
        printf("\n");
    }

    printf("----\n");

    for(int i=0; i<n2; i++) {
        for(int j=0; j<2; j++) {
            printf("%d ", l2[i][j]);
        }
        printf("\n");
    }
}
