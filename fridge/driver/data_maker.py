def make_mcnp_problem(assembly):
    assembly.material.num_particles_per_gen = 10e5
    assembly.material.num_gens = 250
    assembly.material.num_skipped_gens = 50
    assembly.material.ksrc = [0, 0, assembly.assembly_data.ix['height', 'assembly']]
    kopts = ''
    if assembly.material.kopts:
        kopts = 'kopts BLOCKSIZE=10 KINETICS=YES PRECURSOR=Yes \n'

    kcode_output = 'kcode ' + str(assembly.material.num_particles_per_gen) + " 1.0 " + \
                   str(assembly.material.num_skipped_gens) + " " + str(assembly.material.num_gens) + '\n'
    ksrc_output = 'ksrc ' + str(assembly.material.ksrc[0]) + " " + str(assembly.material.ksrc[1]) + " " + \
                  str(assembly.material.ksrc[2]/3) + '\n'
    prdmp_output = 'PRDMP 100 10 100 1 \n'

    mcnp_output = kcode_output + ksrc_output + prdmp_output + kopts
    return mcnp_output