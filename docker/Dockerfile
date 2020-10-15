FROM sbrg/masspy:0.1.1 AS setup
USER root

ENV EXAMPLES_DIR=${HOME}/mass_project/MASSpy-publication

WORKDIR ${HOME}/tmp
RUN git clone https://github.com/SBRG/MASSpy-publication.git '--quiet' .
WORKDIR ${EXAMPLES_DIR}

# Image only for validation example
FROM setup AS validation

# Copy example, remove tmp, and setup entrypoint.
COPY --from=setup ${HOME}/tmp/validation ${EXAMPLES_DIR}/validation/
WORKDIR ${HOME}
RUN rm -rf tmp

USER ${USER}

WORKDIR ${HOME}/mass_project/
ENTRYPOINT [ "../opt/docker-scripts/docker-entrypoint.sh" ]
CMD [ "sh" ]

# Image only for ensemble modeling demonstration
FROM setup AS ensemble-modeling

# Copy example, remove tmp, and setup entrypoint.
COPY --from=setup ${HOME}/tmp/ensemble-modeling ${EXAMPLES_DIR}/ensemble-modeling/
WORKDIR ${HOME}
RUN rm -rf tmp

USER ${USER}

WORKDIR ${HOME}/mass_project/
ENTRYPOINT [ "../opt/docker-scripts/docker-entrypoint.sh" ]
CMD [ "sh" ]

# Image only for case study
FROM setup AS case-study

# Copy example, remove tmp, and setup entrypoint.
COPY --from=setup ${HOME}/tmp/case-study ${EXAMPLES_DIR}/case-study/
WORKDIR ${HOME}
RUN rm -rf tmp

USER ${USER}

WORKDIR ${HOME}/mass_project/
ENTRYPOINT [ "../opt/docker-scripts/docker-entrypoint.sh" ]
CMD [ "sh" ]

# Image for entire publication
FROM setup AS all 
# Copy examples, remove tmp, and setup entrypoint.
WORKDIR ${HOME}

COPY --from=validation ${EXAMPLES_DIR} ${EXAMPLES_DIR}/
COPY --from=ensemble-modeling ${EXAMPLES_DIR} ${EXAMPLES_DIR}/
COPY --from=case-study ${EXAMPLES_DIR} ${EXAMPLES_DIR}/

WORKDIR ${HOME}
RUN rm -rf tmp

USER ${USER}

WORKDIR ${HOME}/mass_project/
ENTRYPOINT [ "../opt/docker-scripts/docker-entrypoint.sh" ]
CMD [ "sh" ]