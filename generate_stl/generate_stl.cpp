#include <stdio.h>

void twoLayerTriangles(int l1[][2], int n1, int z1, int l2[][2], int n2, int z2);

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
        
    twoLayerTriangles(l1, n1, 100, l2, n2, 101);

    return 0;
}

void addTriangle(int triangle[][3], int xy1[2], int z1, int xy2[2], int z2, int xy3[2], int z3) {
    triangle[0][0] = xy1[0];
    triangle[0][1] = xy1[1];
    triangle[0][2] = z1;

    triangle[1][0] = xy2[0];
    triangle[1][1] = xy2[1];
    triangle[1][2] = z2;

    triangle[2][0] = xy3[0];
    triangle[2][1] = xy3[1];
    triangle[2][2] = z3;
}

void printTriangle(int tri[][3]) {
    for(int i=0; i<3; i++) {
        printf("[");
        for(int j=0; j<3; j++) {
            printf("%d,", tri[i][j]);
        }
        printf("] ");
    }
    printf("\n");
}

int getDist(int a[2], int b[2]) {
    // note: this function returns distance squared, but that's ok for our comparison
    int dx = a[0] - b[0];
    int dy = a[1] - b[1];
    return dx*dx + dy*dy;
}

void twoLayerTriangles(int l1[][2], int n1, int z1, int l2[][2], int n2, int z2) {
    int triangles[n1+n2+1][3][3];
    
    int done = 0; 
    int i1 = 0;
    int i2 = 0;

    while(!done) {
        if(i1<n1-1 && i2<n2-1) {
            int d12 = getDist(l1[i1], l2[i2+1]);
            int d21 = getDist(l2[i2], l1[i1+1]);

            if(d12 < d21) {
               addTriangle(triangles[i1+i2], l1[i1], z1, l2[i2], z2, l2[i2+1], z2);
               printTriangle(triangles[i1+i2]);
               i2++;
            } else {
               addTriangle(triangles[i1+i2], l1[i1], z1, l2[i2], z2, l1[i1+1], z1);
               printTriangle(triangles[i1+i2]);
               i1++;
            }
        } else {
            done = 1;
        }
    }
}
