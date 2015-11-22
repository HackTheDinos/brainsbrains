
all: test_triangles libtriangle.so

default: all

test_triangles: buildTwoLayerTriangles.c test_triangles.c
	gcc -O3 -o test_triangles test_triangles.c buildTwoLayerTriangles.c -lm

libtriangle.so: buildTwoLayerTriangles.c
	gcc -fPIC -O3 -shared -o libtriangle.so buildTwoLayerTriangles.c

clean:
	rm -f test_triangles libtriangle.so
