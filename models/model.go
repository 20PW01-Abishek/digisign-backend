package models

type Pdf struct {
	ID         int `json:"ID"`
	FileName   string `json:"filename"`
	UploaderID int `json:"uploader_id"`
}

func SamplePdf() []Pdf {
	var pdfs1 = []Pdf{
		{ID: 1, FileName: "20pw01", UploaderID: 1},
	}
	return pdfs1
}
