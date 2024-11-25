package services



import (
	"github.com/mezni/bridge/cdrgen/internal/domain/interfaces"
	"github.com/mezni/bridge/cdrgen/internal/domain/services"
)

// DummyServiceApp is the application service that uses the DummyService
type DummyServiceApp struct {
	dummyService *domain.DummyService
}

// NewDummyServiceApp creates a new instance of DummyServiceApp
func NewDummyServiceApp(dummyService *domain.DummyService) *DummyServiceApp {
	return &DummyServiceApp{
		dummyService: dummyService,
	}
}

// ExecuteDummyService calls the DoNothing method on the DummyService
func (app *DummyServiceApp) ExecuteDummyService() {
	app.dummyService.DoNothing()
}
