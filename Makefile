INSTALL_DIR=/usr/local

libdropbox_ext4.so: dropbox_ext4.o
	$(LD) -shared -ldl -o $@ $^ && strip $@

%.o: %.c
	$(CC) -fPIC -D_GNU_SOURCE -Wall -Os -o $@ -c $<

clean:
	rm -f *.o *.so

install: libdropbox_ext4.so
	install $^ $(INSTALL_DIR)/lib/ && \
	echo -e "#!/bin/bash\n\nLD_PRELOAD=$(INSTALL_DIR)/lib/$^ exec /usr/bin/dropbox \"\$$@\"" > $(INSTALL_DIR)/bin/dropbox && \
	chmod 0755 $(INSTALL_DIR)/bin/dropbox

uninstall:
	rm -f $(INSTALL_DIR)/bin/dropbox && \
	rm -f $(INSTALL_DIR)/lib/libdropbox_ext4.so
