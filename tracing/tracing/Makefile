PROTOC=protoc

PY_PROTOS=histogram_pb2.py
all: $(PY_PROTOS)

%_pb2.py: proto/%.proto
	$(PROTOC) -Iproto -I. --python_out=. $<

.PHONY: clean

clean:
	rm -f $(PY_PROTOS)

