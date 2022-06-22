All:
	g++ hwserver.c -lzmq -o hwserver
clean:
	rm hwserver
install:
	sudo apt-get install libczmq-dev
mem:
	valgrind --tool=memcheck --leak-check=full  ./hwserver
