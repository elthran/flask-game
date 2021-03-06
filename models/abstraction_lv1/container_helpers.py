{% macro build_container(cls_name, back_populates, data, no_container=False) %}
{% set names = get_names(data) %}
{% set container_name = cls_name + "Container" %}
{% set container_table_name = cls_name.lower() + "_container" %}
{% set attrib_names = normalize_attrib_names(names) %}
{% set class_names = normalize_class_names(names) %}
ALL_NAMES = {{ names }}
ALL_ATTRIBUTE_NAMES = {{ attrib_names }}
ALL_CLASS_NAMES = {{ class_names }}
{% if no_container %}
{% else %}


class {{ container_name }}(Base):
    # Relationships
    # Hero to self is one to one.
    hero_id = Column(Integer, ForeignKey('hero.id', ondelete="CASCADE"))
    hero = relationship("Hero", back_populates="{{ back_populates }}")

    # Container connections are one to one.
    {% for name in attrib_names %}
    {% set class_name = class_names[loop.index0] %}
    {{ name }} = relationship(
        "{{ class_name }}",
        primaryjoin="and_({{ container_name }}.id=={{ cls_name }}.{{ container_table_name }}_id, "
                    "{{ cls_name }}.name=='{{ class_name }}')",
        uselist=False,
        cascade="all, delete-orphan")
    {% endfor %}

    def __init__(self):
        {% for name in attrib_names %}
        self.{{ name }} = {{ class_names[loop.index0] }}()
        {% endfor %}

    def items(self):
        """Basically a dict.items() clone that looks like ((key, value),
            (key, value), ...)

        This is an iterator? Maybe it should be a list or a view?
        """
        return ((key, getattr(self, key)) for key in ALL_ATTRIBUTE_NAMES)

    def __iter__(self):
        """Return all the attributes of this function as an iterator."""
        return (getattr(self, key) for key in ALL_ATTRIBUTE_NAMES)
{% endif %}
{% endmacro %}
