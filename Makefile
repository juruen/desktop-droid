all: desktop_droid

.PHONY: desktop_droid
desktop_droid:
	$(MAKE) -C $(CURDIR)/desktop_droid

clean:
	$(MAKE) -C $(CURDIR)/desktop_droid clean

pep8:
	pep8 --repeat --exclude=ui .
