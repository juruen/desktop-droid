all: ui desktop_droid_qrc.py

.PHONY: ui
ui:
	$(MAKE) -C $(CURDIR)/ui all

desktop_droid_qrc.py: desktop_droid.qrc
	pyrcc4 -o desktop_droid_qrc.py desktop_droid.qrc

clean:
	$(MAKE) -C $(CURDIR)/ui clean
	rm *.pyc || true
	rm desktop_droid_qrc.py || true

