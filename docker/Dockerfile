FROM sbrg/masspy:0.1.1 AS setup
USER root

# Remove documentation from image to reduce size before adding publication files
WORKDIR ${HOME}/opt/MASSpy
RUN rm -rf docs

ENV EXAMPLES_DIR=${HOME}/mass_project/MASSpy-publication

WORKDIR ${HOME}/tmp
# Clone Git directory and install dependencies using requirements file
RUN echo \
    && git clone https://github.com/SBRG/MASSpy-publication.git '--quiet' . \
    # Install xlrd to read and write Excel Sheets with pandas
    && pip install xlrd '--quiet' --no-cache-dir \
    # Install simplejson for improved performance with JSON files
    && pip install simplejson '--quiet' --no-cache-dir

WORKDIR ${EXAMPLES_DIR}

# Image only for validation example
FROM setup AS validation

# Copy example, remove tmp, and setup entrypoint.
COPY --from=setup ${HOME}/tmp/validation ${EXAMPLES_DIR}/validation/

# Finish image on assumption it is final
WORKDIR ${HOME}
RUN rm -rf tmp
RUN echo \
    && chown -R ${USER} ${EXAMPLES_DIR}/ \
    && chmod -R 777 ${EXAMPLES_DIR}/
USER ${USER}
WORKDIR ${EXAMPLES_DIR}
ENTRYPOINT [ "../../opt/docker-scripts/docker-entrypoint.sh" ]
CMD [ "sh" ]

# Image only for ensemble modeling demonstration
FROM setup AS ensemble-modeling

# Copy example, remove tmp, and setup entrypoint.
COPY --from=setup ${HOME}/tmp/ensemble-modeling ${EXAMPLES_DIR}/ensemble-modeling/
# Finish image on assumption it is final
WORKDIR ${HOME}
RUN rm -rf tmp
RUN echo \
    && chown -R ${USER} ${EXAMPLES_DIR}/ \
    && chmod -R 777 ${EXAMPLES_DIR}/
USER ${USER}
WORKDIR ${EXAMPLES_DIR}
ENTRYPOINT [ "../../opt/docker-scripts/docker-entrypoint.sh" ]
CMD [ "sh" ]

# Image only for case study
FROM setup AS case-study

# Copy example, remove tmp, and setup entrypoint.
COPY --from=setup ${HOME}/tmp/case-study ${EXAMPLES_DIR}/case-study/
# Finish image on assumption it is final
WORKDIR ${HOME}
RUN rm -rf tmp
RUN echo \
    && chown -R ${USER} ${EXAMPLES_DIR}/ \
    && chmod -R 777 ${EXAMPLES_DIR}/
USER ${USER}
WORKDIR ${EXAMPLES_DIR}
ENTRYPOINT [ "../../opt/docker-scripts/docker-entrypoint.sh" ]
CMD [ "sh" ]

# Image for entire publication
FROM setup AS all 
# Copy examples, remove tmp, and setup entrypoint.
WORKDIR ${HOME}

COPY --from=validation ${EXAMPLES_DIR} ${EXAMPLES_DIR}/
COPY --from=ensemble-modeling ${EXAMPLES_DIR} ${EXAMPLES_DIR}/
COPY --from=case-study ${EXAMPLES_DIR} ${EXAMPLES_DIR}/

# Finish image
WORKDIR ${HOME}
RUN rm -rf tmp
RUN echo \
    && chown -R ${USER} ${EXAMPLES_DIR}/ \
    && chmod -R 777 ${EXAMPLES_DIR}/
USER ${USER}
WORKDIR ${EXAMPLES_DIR}
ENTRYPOINT [ "../../opt/docker-scripts/docker-entrypoint.sh" ]
CMD [ "sh" ]