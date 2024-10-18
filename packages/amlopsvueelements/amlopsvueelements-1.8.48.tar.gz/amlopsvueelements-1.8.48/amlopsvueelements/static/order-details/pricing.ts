import type { IPkTypeReference } from '../general.types';
import type { IPerson } from '../order/order-reference.types';

export interface ICurrency {
  code: string;
  symbol: string;
  division_name: string;
  division_factor: number;
}

export interface ICurrencyRate {
  src: string;
  rate: string;
  timestamp: number;
}

export interface ICurrencyRates {
  [key: string]: ICurrencyRate;
}

export interface IPricingUnit {
  pk: number;
  description: string;
  description_short: string;
  currency_division_used: boolean;
}

export interface ISupplierFuel {
  created_at: string;
  created_by: IPerson;
  id: number;
  results: Array<{
    key: string;
    is_expired: false;
    expiration_date: string | null;
    color: string;
    fuel_type: IPkTypeReference;
    supplier: {
      pk: number;
      full_repr: string;
      registered_name: string;
    };
    ipa: {
      pk: number;
      full_repr: string;
      registered_name: string;
    };
    handler: IPkTypeReference;
    excluded_handlers: [];
    delivery_method: object | null;
    excluded_delivery_methods: [];
    apron: object | null;
    excluded_aprons: Array<object>;
    terminal: object | null;
    excluded_terminals: Array<object>;
    total_uplift_cost: string;
    client_total_uplift_cost: string;
    currency: ICurrency;
    issues: Array<string>;
    tax_notes: {
      official: {
        [key: string]: Array<string>;
      };
      supplier: {
        [key: string]: Array<string>;
      };
    };
  }>;
  scenario: {
    mode: string;
    apron: object | null;
    airport: {
      pk: number;
      icao: string;
      full_repr: string;
      registered_name: string;
    };
    handler: object | null;
    currency: ICurrency;
    date_utc: string;
    from_api: true;
    fuel_cat: IPkTypeReference;
    is_rerun: boolean;
    terminal: object | null;
    used_plds: Array<number>;
    is_private: boolean;
    uplift_qty: string;
    uplift_uom: {
      pk: number;
      code: string;
      description: string;
      description_plural: string;
    };
    destination: object | null;
    flight_type: {
      code: string;
      name: string;
    };
    override_xr: boolean;
    datetime_utc: string;
    is_defueling: boolean;
    aircraft_type: {
      pk: number;
    };
    is_fuel_taken: true;
    specific_client: {
      pk: number;
      full_repr: string;
      registered_name: string;
    };
    uplift_datetime: string;
    client_hierarchy: Array<{
      pk: number;
      full_repr: string;
      registered_name: string;
    }>;
    is_international: boolean;
    is_multi_vehicle: boolean;
    overwing_fueling: boolean;
    uplift_time_type: string;
    validity_date_utc: string;
    inc_client_pricing: boolean;
    used_agreement_ids: Array<number>;
    used_currency_rates: ICurrencyRates;
    earliest_expiry_date: string;
    pricing_unit_usd_usg: IPricingUnit;
    validity_datetime_lt: string;
    prevent_notams_update: boolean;
    validity_datetime_utc: string;
    published_pricing_only: boolean;
    applicable_destinations: Array<string>;
    applicable_flight_types: Array<string>;
    using_representative_ac_type: boolean;
    extend_expired_agreement_client_pricing: boolean;
  };
}

export interface ISupplierFuelDetails {
  ipa: {
    pk: number;
    full_repr: string;
    registered_name: string;
  };
  key: string;
  fees: {
    list: {
      [key: string]: {
        obj: number;
        uom: {
          pk: number;
          code: string;
          description: string;
          description_plural: string;
        };
        notes: string[];
        amount: string;
        obj_type: string;
        unit_price: string;
        display_name: string;
        client_amount: string;
        price_usd_usg: object | null;
        agreement_pricing: boolean;
        client_unit_price: string;
        original_currency: ICurrency;
        converted_uplift_qty: object | null;
        original_pricing_unit: IPricingUnit;
        is_fuel_price_percentage: boolean;
      };
    };
    total: string;
    issues: string[];
    client_total: string;
    currency_rates: ICurrencyRates;
    agreement_pricing: boolean;
  };
  taxes: {
    list: {
      [key: string]: {
        official: {
          amount: string;
          components: Array<{
            obj: number;
            uom: object | null;
            base: string | null;
            amount: number;
            obj_type: string;
            tax_level: string;
            percentage: string | null;
            unit_price: string | null;
            client_base: string | null;
            is_variable: boolean;
            base_fee_cat: object | null;
            client_amount: number;
            price_usd_usg: {
              base_usd_usg: string;
              rate_usd_usg: string;
            } | null;
            inc_in_pricing: boolean;
            base_components: {
              fuel: boolean;
              fees?: {
                [key: string]: string;
              };
            };
            exemption_applied: boolean;
            original_currency: ICurrency;
            variable_comments: string[];
            exemption_doc_types: string;
            converted_uplift_qty: string | null;
            original_pricing_unit: IPricingUnit | null;
          }>;
          client_amount: string;
        };
        supplier: {
          amount: string;
          components: Array<{
            obj: number;
            uom: object | null;
            base: number | null;
            amount: number;
            obj_type: string;
            tax_level: string;
            percentage: string | null;
            unit_price: string | null;
            client_base: string | null;
            is_variable: boolean;
            base_fee_cat: object | null;
            client_amount: number;
            price_usd_usg: {
              base_usd_usg: string;
              rate_usd_usg: string;
            } | null;
            inc_in_pricing: boolean;
            base_components: {
              fuel: boolean;
              fees?: {
                [key: string]: string;
              };
            };
            exemption_applied: boolean;
            original_currency: ICurrency;
            variable_comments: string[];
            exemption_doc_types: string;
            converted_uplift_qty: string | null;
            original_pricing_unit: IPricingUnit | null;
          }>;
          client_amount: string;
        };
        row_highlight_class: string;
      };
    };
    total: string;
    issues: string[];
    comparison: boolean;
    client_total: string;
    currency_rates: ICurrencyRates;
    official_total: string;
    supplier_total: string;
  };
  total: string;
  issues: string[];
  notams: Array<{
    pk: number;
    text: string;
    status: string;
    effective_end: string | null;
    effective_start: string;
  }>;
  status: string;
  airport: {
    pk: number;
    icao: string;
    full_repr: string;
    registered_name: string;
  };
  row_key: number[];
  aml_fees: {
    list: Record<string, never>;
    total: string;
  };
  currency: ICurrency;
  supplier: {
    pk: number;
    full_repr: string;
    registered_name: string;
  };
  fuel_type: IPkTypeReference;
  fuel_price: {
    obj: {
      pk: number;
      price: string;
    };
    uom: {
      pk: number;
      code: string;
      description: string;
      description_plural: string;
    };
    fuel: IPkTypeReference;
    notes: string[];
    amount: string;
    is_pap: object | null;
    issues: string[];
    obj_type: string;
    unit_price: string;
    pricing_url: string;
    pricing_link: string;
    client_amount: string;
    currency_rates: ICurrencyRates;
    fuel_index_obj: {
      pk: number;
      price: string;
      valid_to: string | null;
      is_primary: boolean;
      valid_from: string;
      pricing_unit: IPricingUnit;
      fuel_index_details: {
        pk: number;
        repr: string;
        fuel_index: {
          pk: number;
          repr: string;
        };
      };
      source_organisation: {
        pk: number;
        full_repr: string;
        registered_name: string;
      };
    };
    base_pricing_url: string | null;
    discount_applied: object | null;
    agreement_pricing: boolean;
    client_unit_price: string;
    original_currency: ICurrency;
    diff_price_usd_usg: string;
    bench_price_usd_usg: string;
    final_price_usd_usg: string;
    market_pricing_base: string | null;
    pricing_desc_suffix: string;
    converted_uplift_qty: string;
    original_pricing_unit: IPricingUnit;
  };
  band_end_usg: object | null;
  client_terms: {
    pk: number;
    comments: object | null;
    account_number: string;
    payment_terms_days: number;
  };
  client_total: string;
  band_start_usg: object | null;
  delivery_method: IPkTypeReference | null;
  excluded_aprons: object[];
  expiration_date: object | null;
  agreement_pricing: boolean;
  excluded_handlers: object[];
  notams_last_check: string;
  additional_classes: string;
  excluded_terminals: object[];
  used_currency_rates: ICurrencyRates;
  total_official_taxes: string;
  intermediate_supplier: {
    pk: number;
    full_repr: string;
    registered_name: string;
  } | null;
  apron_specific_pricing: IPkTypeReference | null;
  terminal_specific_pricing: IPkTypeReference | null;
  client_specific_pricing: IPkTypeReference | null;
  used_supplier_uom_rates: object;
  handler_specific_pricing: IPkTypeReference;
}

export interface IPricingUnit {
  unit_code: string;
  description_short: string;
  description: string;
  uom: {
    id: number;
    description: string;
    description_plural: string;
    code: string;
  };
  currency: {
    id: number;
    code: string;
    name: string;
    name_plural: string;
    symbol: string;
    division_name: string;
    division_factor: number;
  };
  currency_division_used: boolean;
}

export interface ITax {
  applicable_country: {
    id: number;
    name: string;
  };
  applicable_region: object | null;
  local_name: string;
  short_name: string;
  category: {
    id: number;
    name: string;
  };
}

export interface IFee {
  supplier: ISupplierClientFee;
  client: ISupplierClientFee;
}

export interface ISupplierClientFee {
  id: number;
  quantity_value: string;
  quantity_uom: object | null;
  unit_price_amount: string;
  unit_price_pricing_unit: IPricingUnit;
  amount_total: string;
  amount_currency: ICurrency;
  suppliers_fuel_pricing_market_row: object | null;
  suppliers_fuel_agreements_pricing_manual_row: object | null;
  suppliers_fuel_agreements_pricing_formulae_row: object | null;
  fuel_indices_pricing: object | null;
  suppliers_fuel_fees_rates_row: {
    supplier_fuel_fee: {
      fuel_fee_category: IPkTypeReference;
    };
  } | null;
}

export interface ITaxInfo {
  supplier: ISupplierClientTax;
  client: ISupplierClientTax;
}

export interface ISupplierClientTax {
  tax_percentage: string | null;
  tax_unit_rate: string | null;
  tax_application_method: {
    id: number;
    fuel_pricing_unit: IPricingUnit;
  } | null;
  tax_amount_total: string;
  tax_amount_currency: ICurrency;
  tax: ITax;
  tax_source: string;
  tax_applicability: string;
  applies_on: {
    fuel?: boolean;
    fees?: string[];
    taxes?: string;
  };
}

export interface IFuelPricing {
  supplier: ISupplierClient;
  client: ISupplierClient;
}

export interface ISupplierClient {
  id: number;
  quantity_value: string;
  quantity_uom: {
    id: number;
    description: string;
    description_plural: string;
    code: string;
  };
  unit_price_amount: string;
  unit_price_pricing_unit: IPricingUnit;
  amount_total: string;
  amount_currency: ICurrency;
  suppliers_fuel_pricing_market_row: object | null;
  suppliers_fuel_agreements_pricing_manual_row: object | null;
  suppliers_fuel_agreements_pricing_formulae_row: {
    id: number;
    index_period_is_lagged: boolean;
    index_period_is_grace: boolean;
  } | null;
  fuel_indices_pricing: IFuelIndexPricing | null;
  suppliers_fuel_fees_rates_row: object | null;
}

export interface IFuelIndexPricing {
  id: number;
  fuel_index_details: {
    id: number;
    fuel_index: {
      id: number;
      name: string;
      provider: {
        id: number;
        tiny_repr: string;
        short_repr: string;
        full_repr: string;
        details: {
          registered_name: string;
          trading_name: string | null;
          type: {
            id: number;
            name: string;
          };
        };
      };
    };
    structure_description: string;
  };
  price: string;
  pricing_unit: IPricingUnit;
  is_primary: boolean;
  source_organisation: {
    id: number;
    tiny_repr: string;
    short_repr: string;
    full_repr: string;
    details: {
      registered_name: string;
      trading_name: string | null;
      type: {
        id: number;
        name: string;
      };
    };
  };
  updated_at: string;
  updated_by: number;
}

export interface IPricingSummary {
  supplier_total: string;
  client_total: string;
  margin_amount: string;
  margin_percentage: number;
}

export interface IFuelPricingObj {
  supplier_id: number;
  fuel_pricing: IFuelPricing;
  fees: IFee[];
  taxes: ITaxInfo[];
  terms_days: {
    client_terms_days: number;
    supplier_terms_days: number;
  };
  pricing_summary: IPricingSummary;
}
