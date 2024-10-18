// SPDX-FileCopyrightText: Contributors to the Power Grid Model project <powergridmodel@lfenergy.org>
//
// SPDX-License-Identifier: MPL-2.0

#define PGM_IO_DLL_EXPORTS

#include <power_grid_model_io_native/vnf_converter/vnf_pgm_converter.hpp>

#include "handle.hpp"
#include <power_grid_model_io_native_c/basics.h>
#include <power_grid_model_io_native_c/vnf_pgm_converter.h>

#include <power_grid_model/auxiliary/dataset.hpp>

using power_grid_model::ConstDataset;

struct PGM_IO_VnfConverter : public PgmVnfConverter {
    using PgmVnfConverter::PgmVnfConverter;
};

// TODO(Laurynas-Jagutis) add call_with_catch for these functions.
PGM_IO_VnfConverter* PGM_IO_create_vnf_converter(const PGM_IO_Handle* /*handle*/, char* file_buffer) {
    auto* converter = new PGM_IO_VnfConverter(file_buffer);
    parse_vnf_file_wrapper(converter);
    return converter;
}

char const* PGM_IO_get_vnf_input_data(const PGM_IO_Handle* /*handle*/, PGM_IO_VnfConverter* converter_ptr) {
    return convert_input_wrapper(converter_ptr).c_str();
}

void PGM_IO_destroy_vnf_converter(PGM_IO_VnfConverter* converter_ptr) { delete converter_ptr; }
