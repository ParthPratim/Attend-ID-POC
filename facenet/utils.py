class Args:

    _mode = None
    _model = None
    _batch_size = None
    _image_size = None
    _classifier_filename = None
    _imgs = None
    _labels = None
    _seed = 666
    _class_names = None

    @property
    def class_names(self):
        return self._class_names
    @property
    def seed(self):
        return self._seed
    @property
    def mode(self):
        return self._mode
    @property
    def model(self):
        return self._model
    @property
    def batch_size(self):
        return self._batch_size
    @property
    def image_size(self):
        return self._image_size
    @property
    def classifier_filename(self):
        return self._classifier_filename
    @property
    def imgs(self):
        return self._imgs
    @property
    def labels(self):
        return self._labels

    @mode.setter
    def mode(self,md):
        self._mode = md
    @model.setter
    def model(self,md):
        self._model = md
    @batch_size.setter
    def batch_size(self,md):
        self._batch_size = md
    @image_size.setter
    def image_size(self,md):
        self._image_size = md
    @classifier_filename.setter
    def classifier_filename(self,md):
        self._classifier_filename = md
    @imgs.setter
    def imgs(self,md):
        self._imgs = md
    @labels.setter
    def labels(self,md):
        self._labels = md
    @class_names.setter
    def class_names(self,md):
        self._class_names = md
