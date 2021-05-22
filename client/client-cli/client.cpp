#include <iostream>
#include <signal.h>
#include <fstream>
#include <streambuf>
#include "TCPClient.h"

TCPClient tcp;

void sig_exit(int s)
{
	tcp.exit();
	exit(0);
}

string read_file(string filename)
{
    ifstream file(filename);
    string str;

    file.seekg(0, ios::end);
    str.reserve(file.tellg());
    file.seekg(0, ios::beg);

    str.assign((istreambuf_iterator<char>(file)), istreambuf_iterator<char>());

    return str;
}

int main(int argc, char *argv[])
{
	if(argc != 4) {
		cerr << "Usage: ./client ip port message" << endl;
		return 0;
	}
	signal(SIGINT, sig_exit);

	string message(argv[3]);
	if (message == "file") {
	    message = read_file("solver.m");
	};

	tcp.setup(argv[1],atoi(argv[2]));
	while(1)
	{
		tcp.Send(message);
		string rec = tcp.receive();
		if( rec != "" )
		{
			cout << rec << endl;
		}
		sleep(1);
	}
	return 0;
}
