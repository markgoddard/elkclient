FROM centos
MAINTAINER mgoddard@cray.com
ADD elkclient.py /bin/elkclient
RUN chmod +x /bin/elkclient
CMD ["/bin/sleep", "infinity"]
