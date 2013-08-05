TESTS=testdiskcache.py testdiskcache_script.py

export PYTHONPATH=../dc

all: $(TESTS)
	echo "Done"

$(TESTS):
	./$@

clean:
	rm -f *~ *.pyc 
	rm -rf /tmp/*testdc*

.PHONY: $(TESTS) all
