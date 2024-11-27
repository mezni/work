package repositories

// Repository defines the methods for interacting with the data store.
type CallRecordRepository interface {
	FindAll() ([]CallRecord, error)
	FindByID(id int) (CallRecord, error)
	Save(callRecord CallRecord) error
	Delete(id int) error
}
