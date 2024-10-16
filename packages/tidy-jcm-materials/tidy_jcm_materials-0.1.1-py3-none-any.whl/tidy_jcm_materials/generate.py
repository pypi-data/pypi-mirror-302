from tidy3d import PoleResidue

template = """
Material{{
    Name = "{name}"
    DomainId = {domain_id}
    RelPermittivity{{
        Constant = {eps_inf}
        {poles}
    }}
}}
"""

template_pole = """
        GeneralizedLorentzPole{{
            Amplitude = {sigma}
            ResonanceFrequency = {omega}
        }}
"""


def jcm_cplx(num: complex) -> str:
    """Format a complex number to be JCM compatible"""
    return f"({num.real}, {num.imag})"


def gen_material(
    material: PoleResidue, name: str = "TidyMaterial", domain_id: int | list[int] = 1
) -> str:
    """Generate JCM compatible GeneralizedLorentzPole model
    from tidy3d.PoleResidue model

    Args:
        material (PoleResidue): the tidy3d material (i.e. from their database)

    Returns:
        str: the 'Material' section that needs to be added to the materials.jcm
    """

    poles = ""
    for pole, res in material.poles:
        poles += template_pole.format(sigma=jcm_cplx(res), omega=jcm_cplx(1j * pole))

    return template.format(
        name=name, domain_id=domain_id, eps_inf=jcm_cplx(material.eps_inf), poles=poles
    )


if __name__ == "__main__":
    from tidy3d import material_library

    print(gen_material(material_library["Ag"]["JohnsonChristy1972"]))
