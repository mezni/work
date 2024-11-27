package application

import (
	"github.com/mezni/bridge/tools/cdrgen/internal/domain/services"
)

// DummyServiceApp is the application service that uses the DummyService
type DummyServiceApp struct {
	dummyService *services.DummyService
}

// NewDummyServiceApp creates a new instance of DummyServiceApp
func NewDummyServiceApp(dummyService *services.DummyService) *DummyServiceApp {
	return &DummyServiceApp{
		dummyService: dummyService,
	}
}

// ExecuteDummyService calls the DoNothing method on the DummyService
func (app *DummyServiceApp) ExecuteDummyService() {
	app.dummyService.DoNothing()
}
