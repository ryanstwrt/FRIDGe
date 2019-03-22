def make_mcnp_problem(global_vars):
    kopts_output = ''
    if global_vars.kopts:
        kopts_output = 'kopts BLOCKSIZE=10 KINETICS=YES PRECURSOR=Yes \n'

    kcode_output = 'kcode ' + str(global_vars.number_particles_generation) + " 1.0 " + \
                   str(global_vars.number_skipped_generations) + " " + str(global_vars.number_generations) + '\n'
    ksrc_output = 'ksrc 0 0 80 \n'
    prdmp_output = 'PRDMP 100 10 100 1 \n'

    mcnp_output = kcode_output + ksrc_output + prdmp_output + kopts_output
    return mcnp_output
