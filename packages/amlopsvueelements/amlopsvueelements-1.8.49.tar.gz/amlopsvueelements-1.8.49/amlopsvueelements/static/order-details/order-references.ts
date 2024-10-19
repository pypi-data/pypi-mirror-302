import Api from '@/services';
import type { IAircraftLocations, IAirportLocations } from '@/types/order-details/order-details';
import type { IPaginatedResponse, ITypeReference } from '@/types/general.types';
import type {
  IFuelUnit,
  IOrganisation,
  IPerson,
  IService
} from '@/types/order/order-reference.types';
import type { IAircraft, IAircraftTypeEntity } from '@/types/order/aircraft.types';
import type { IAirport } from '@/types/order/airport.types';
import { getIsAdmin } from '@/helpers';
import type {
  IClient,
  IGroundHandler,
  IOperator,
  IOrder,
  IOrderNote,
  IOrderStatus,
  IOrderType
} from '@/types/order/order.types';
import type { ISupplierFuelDetails } from 'shared/types';
import { withErrorHandling } from '@/helpers/errors';
import type { IFuelPricingObj, ISupplierFuel } from 'shared/types';
// import type { ISupplierFuelDetails } from 'shared/types';

class OrderReferenceService extends Api {
  async fetchOrderStatuses() {
    return withErrorHandling(async () => {
      const { data } = await this.get<IOrderStatus[]>(`api/v1/orders/order_statuses/?search=`);
      return typeof data === 'object' ? data : [];
    })();
  }

  async fetchOrderTypes() {
    return withErrorHandling(async () => {
      const { data } = await this.get<IOrderType[]>(`api/v1/orders/order_types/`);
      return data;
    })();
  }

  async fetchOrganisations(search?: string) {
    return withErrorHandling(async () => {
      const {
        data: { results: organisations }
      } = await this.get<IPaginatedResponse<IOrganisation[]>>('api/v1/admin/organisations/', {
        params: { search, 'page[size]': 999 }
      });
      return organisations;
    })();
  }

  async fetchOrganisationPeople(organisationId: number) {
    return withErrorHandling(async () => {
      if (!organisationId) return [];
      const url = `api/v1/organisations/${organisationId}/people/`;
      const { data } = await this.get<IPerson[]>(url);
      return data.map((item) => ({
        ...item,
        display: `${item.details.full_name} (${item.jobs[0]?.job_title})`,
        display_email: `${item.details.full_name} ${item.details.contact_email}`
      }));
    })();
  }

  async fetchAircraftTypes(organisationId: number) {
    return withErrorHandling(async () => {
      if (getIsAdmin() && !organisationId) return [];
      const url = getIsAdmin()
        ? `api/v1/admin/organisation/${organisationId}/aircraft_types/`
        : `api/v1/organisation/aircraft_types/`;
      const {
        data: { data }
      } = await this.get<{ data: IAircraftTypeEntity[] }>(url);
      return data.map((el) => ({
        ...el,
        full_repr: `${el.attributes.manufacturer} ${el.attributes.model} (${el.attributes.designator})`
      }));
    })();
  }

  async fetchAircrafts(organisationId: number) {
    return withErrorHandling(async () => {
      if (!organisationId) return [];
      const url = `api/v1/aircraft/`;
      const { data } = await this.get<IAircraft[]>(url, {
        params: { operator: organisationId }
      });
      return data;
    })();
  }

  async fetchAirportLocations(search?: string | number) {
    return withErrorHandling(async () => {
      const {
        data: { results: airports }
      } = await this.get<IPaginatedResponse<IAirport[]>>('api/v1/organisations/', {
        params: {
          search,
          type: 8,
          optional_fields: 'country'
        }
      });
      return airports;
    })();
  }

  async fetchFuelQuantityUnits() {
    return withErrorHandling(async () => {
      const { data } = await this.get<IFuelUnit[]>('api/v1/uom/');
      return data;
    })();
  }

  async fetchFuelCategories() {
    return withErrorHandling(async () => {
      const { data } = await this.get<ITypeReference[]>('api/v1/fuel_categories/');
      return data;
    })();
  }

  async fetchGroundHandlers(airportId: number) {
    return withErrorHandling(async () => {
      const {
        data: { results: handlers }
      } = await this.get<IPaginatedResponse<IGroundHandler[]>>('api/v1/organisations/', {
        params: {
          type: 3,
          gh_location: airportId
        }
      });
      return handlers;
    })();
  }

  async fetchClients() {
    return withErrorHandling(async () => {
      const {
        data: { results: clients }
      } = await this.get<IPaginatedResponse<IClient[]>>('api/v1/organisations/', {
        params: {
          type_str: 'client',
          optional_fields: 'client_status_list'
        }
      });
      return clients;
    })();
  }

  async fetchOperators() {
    return withErrorHandling(async () => {
      const {
        data: { results: operators }
      } = await this.get<IPaginatedResponse<IOperator[]>>('api/v1/organisations/', {
        params: {
          type_str: 'operator'
        }
      });
      return operators;
    })();
  }

  async fetchMissionTypes() {
    return withErrorHandling(async () => {
      const { data } = await this.get<ITypeReference[]>('api/v1/admin/handling_requests/types/');
      return data;
    })();
  }

  async fetchPersonTitles() {
    return withErrorHandling(async () => {
      const { data } = await this.get<ITypeReference[]>('api/v1/person_titles/');
      return data;
    })();
  }

  async fetchPersonRoles() {
    return withErrorHandling(async () => {
      const { data } = await this.get<ITypeReference[]>('api/v1/person_roles/');
      return data;
    })();
  }

  async fetchServices(
    locationId?: string | number,
    organisationId?: string | number,
    codeName?: string
  ) {
    return withErrorHandling(async () => {
      const { data } = await this.get<{ data: IService[] }>('api/v1/handling_services/', {
        params: { organisation_id: organisationId, location_id: locationId, codename: codeName }
      });
      return data.data
        ?.filter((service) => {
          return !(
            service.attributes.is_dla &&
            !service.attributes.is_dla_visible_arrival &&
            !service.attributes.is_dla_visible_departure
          );
        })
        .map((service) => ({
          ...service,
          id: Number(service.id)
        }));
    })();
  }

  async fetchMeta() {
    return withErrorHandling(async () => {
      const { data } = await this.get('api/v1/meta/');
      return data;
    })();
  }

  async fetchOrderNotes(orderId: number) {
    return withErrorHandling(async () => {
      const { data } = await this.get<IOrderNote[]>(`api/v1/orders/${orderId}/notes/`);
      return data;
    })();
  }

  async fetchSupplierFuel(order: IOrder): Promise<ISupplierFuel> {
    return withErrorHandling(async () => {
      const { data } = await this.get<ISupplierFuel>(
        `api/v1/pricing/supplier_fuel_pricing/${order.pricing_calculation_record}/`
      );
      return data;
    })();
  }

  async fetchSupplierFuelDetails(
    supplierId: number,
    detailsId: number
  ): Promise<ISupplierFuelDetails> {
    return withErrorHandling(async () => {
      const { data } = await this.get<ISupplierFuelDetails>(
        `api/v1/pricing/supplier_fuel_pricing/${supplierId}/results/${detailsId}/`
      );
      return data;
    })();
  }

  async selectFuelSupplier(orderId: number, payload: any) {
    return withErrorHandling(async () => {
      const { data } = await this.post<any[]>(
        `api/v1/orders/${orderId}/fuel_pricing/from_pricing_record/`,
        payload
      );
      return data;
    })();
  }

  async fetchOrderPricing(orderId: number): Promise<IFuelPricingObj> {
    return withErrorHandling(async () => {
      const { data } = await this.get<any>(`api/v1/orders/${orderId}/fuel_pricing/`);
      return data;
    })();
  }

  async updateOrderPricing(orderId: number, payload: any): Promise<IFuelPricingObj> {
    return withErrorHandling(async () => {
      const { data } = await this.put<IFuelPricingObj>(
        `api/v1/orders/${orderId}/fuel_pricing/`,
        payload
      );
      return data;
    })();
  }

  async updateOrderROI(orderId: number, payload: any) {
    return withErrorHandling(async () => {
      const { data } = await this.post<any[]>(`api/v1/orders/${orderId}/roi/`, payload);
      return data;
    })();
  }

  async fetchFlightAirportLocations(id: number): Promise<IAirportLocations> {
    return withErrorHandling(async () => {
      const { data } = await this.post<any>(`api/v1/sfr_tracking/airport_locations/`, {
        handling_request: id.toString()
      });
      return data;
    })();
  }

  async fetchFlightAircraftLocations(id: number): Promise<IAircraftLocations> {
    return withErrorHandling(async () => {
      const { data } = await this.post<any>(`api/v1/sfr_tracking/aircraft_locations/`, {
        handling_request: id.toString()
      });
      return data;
    })();
  }

  async fetchOrderQuoteButton(orderId: number) {
    return withErrorHandling(async () => {
      const { data } = await this.get<any>(`api/v1/orders/${orderId}/quote_button/`);
      return data;
    })();
  }

  async fetchOrderProceedButton(orderId: number) {
    return withErrorHandling(async () => {
      const { data } = await this.get<any>(`api/v1/orders/${orderId}/proceed_button/`);
      return data;
    })();
  }
}

export default new OrderReferenceService();
