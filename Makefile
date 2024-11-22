GO            = go
GOBUILD       = $(GO) build
GOCLEAN       = $(GO) clean
GOTEST        = $(GO) test
GOGET         = $(GO) get
GOFMT         = $(GO)fmt
GOVET         = $(GO) vet

BINARY        = myapp
#SRC           = $(shell find . -type f -name '*.go')
SRC           = tools/cdrgen/cmd/main.go

all: build

build:
	$(GOBUILD) -o $(BINARY) $(SRC)

clean:
	$(GOCLEAN)
	rm -f $(BINARY)

test:
	$(GOTEST) -v ./...

fmt:
	$(GOFMT) -w $(SRC)

vet:
	$(GOVET) ./...

install:
	$(GOGET) ./...
	$(GO) install ./...

run:
	$(GO) run $(SRC)

docker:
	docker build -t $(BINARY) .